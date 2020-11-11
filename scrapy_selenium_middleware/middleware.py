import logging
from enum import Enum
from typing import Any
from typing import Optional, List

from scrapy import Spider, Request
from scrapy.crawler import Crawler
from scrapy.http import HtmlResponse
from scrapy.signalmanager import SignalManager
from scrapy.signals import spider_closed
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.command import Command
from seleniumwire import webdriver
from seleniumwire.webdriver import Firefox
from twisted.internet.threads import deferToThread

log = logging.getLogger(__name__)

for logger in ("selenium", "seleniumwire"):
    logging.getLogger(logger).setLevel(logging.ERROR)

ignore_http_methods = [
    "OPTIONS",
    "POST",
    "GET",
    "PUT",
    "DELETE",
    "CONNECT",
    "TRACE",
    "PATCH",
]


class RequestMetaKeys(Enum):
    return_value_browser_interaction = (
        "__SELENIUM_MIDDLEWARE_BROWSER_INTERACTION_RETURN_VALUE__"
    )
    use_middleware = "__SELENIUM_MIDDLEWARE_USE_FOR_THIS_REQUEST__"


class SeleniumSpider(Spider):
    def parse(self, response, **kwargs):
        pass

    def browser_interaction_before_get(self, driver: Firefox, request: Request) -> None:
        """
        Override this method to interact with the browser before driver.get(request.url)
        was called in middleware
        """
        pass

    def browser_interaction_after_get(self, driver: Firefox, request: Request) -> Any:
        """
        Override this method to interact with the browser after driver.get(request.url)
        was called in middleware
        :return any value returned from this method will be added to the response meta dict
        with the key "__SELENIUM_MIDDLEWARE_BROWSER_INTERACTION_VALUE__"
        """
        pass


class SeleniumDownloader:
    @classmethod
    def from_crawler(cls, crawler: Crawler):
        instance = cls(
            crawler.settings.getbool("SELENIUM_IS_HEADLESS"),
            crawler.settings.get("SELENIUM_PROXY"),
            crawler.settings.get("SELENIUM_USER_AGENT"),
            crawler.settings.getlist("SELENIUM_REQUEST_RECORD_SCOPE", []),
            crawler.settings.getdict("SELENIUM_FIREFOX_PROFILE_SETTINGS", {}),
            crawler.signals,
            crawler.settings.getint("SELENIUM_PAGE_LOAD_TIMEOUT", 120),
        )

        crawler.signals.connect(instance.spider_closed, spider_closed)
        return instance

    def __init__(
        self,
        is_headless: bool,
        proxy: str,
        user_agent: str,
        request_scope: List[str],
        profile_settings: dict,
        signal: SignalManager,
        selenium_page_load_timeout: int,
    ):
        self.is_headless = is_headless
        self.proxy = proxy
        self.user_agent = user_agent
        self.request_scope = request_scope
        self.profile_settings = profile_settings
        self.selenium_page_load_timeout = selenium_page_load_timeout
        self.__driver: Optional[webdriver.Firefox] = None
        self.signal = signal

    def process_request(self, request: Request, spider: SeleniumSpider):
        if request.meta.get(RequestMetaKeys.use_middleware.value) and isinstance(
            spider, SeleniumSpider
        ):
            return deferToThread(self.download_with_selenium, request, spider)

    def download_with_selenium(
        self, request: Request, spider: SeleniumSpider
    ) -> HtmlResponse:
        driver = self._driver
        driver.set_page_load_timeout(self.selenium_page_load_timeout)
        spider.browser_interaction_before_get(driver, request)
        log.info(
            f"web driver get url: {request.url} timeout : {self.selenium_page_load_timeout}"
        )
        driver.get(request.url)
        data = spider.browser_interaction_after_get(driver, request)
        request.meta[RequestMetaKeys.return_value_browser_interaction.value] = data
        html = self._driver.execute_script(
            'return document.getElementsByTagName("html")[0].outerHTML'
        )
        response = HtmlResponse(
            self._driver.current_url, body=html, encoding="utf-8", request=request
        )
        return response

    @property
    def _driver(self) -> webdriver.Firefox:
        if self.__driver is None:
            log.info("driver is None opening a new driver")
            self.__driver = self._create_driver()
        else:
            try:
                self.__driver.execute(Command.STATUS)
            except Exception:
                log.exception("driver not responding try to close and open new driver")
                try:
                    self.__driver.quit()
                except Exception:
                    log.exception("failed to close driver")
                self.__driver = self._create_driver()

        return self.__driver

    def spider_closed(self):
        if self.__driver is not None:
            try:
                self.__driver.quit()
            except Exception:
                log.exception("failed to close browser on spider close")

    def _create_driver(self) -> webdriver.Firefox:
        profile = webdriver.FirefoxProfile()
        if self.profile_settings:
            for setting, value in self.profile_settings.items():
                profile.set_preference(setting, value)
        if self.user_agent:
            profile.set_preference("general.useragent.override", self.user_agent)
        profile.update_preferences()
        if self.proxy:
            selenium_wire_options = {
                "proxy": {"http": self.proxy, "https": self.proxy},
                "connection_keep_alive": True,
                "connection_timeout": 180,
            }
        else:
            selenium_wire_options = {}
        options = Options()
        options.headless = self.is_headless
        if not self.request_scope:
            selenium_wire_options["ignore_http_methods"] = ignore_http_methods

        driver = webdriver.Firefox(
            profile, options=options, seleniumwire_options=selenium_wire_options,
        )
        if self.request_scope:
            driver.scopes = self.request_scope
        return driver
