[![Latest PyPI version](https://img.shields.io/pypi/v/scrapy-selenium-middleware)](https://pypi.org/project/scrapy-selenium-middleware/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# scrapy-selenium-middleware

## requirements
* This downloader middleware should be used inside an existing [Scrapy](https://scrapy.org/) project
* Install  Firefox and [gekodriver](https://github.com/mozilla/geckodriver/releases) on the machine running this middleware

## pip
* `pip install scrapy-selenium-middleware`
 
## usage example
for a full scrapy project demo please go [here](https://github.com/Tal-Leibman/scrapy-selenium-middleware-example)

The middleware receives its settings from [scrapy project settings](https://docs.scrapy.org/en/latest/topics/settings.html) <br>
in your scrapy project settings.py file add the following settings
```python
DOWNLOADER_MIDDLEWARES = {"scrapy_selenium_middleware.SeleniumDownloader":451}
CONCURRENT_REQUESTS = 2
SELENIUM_IS_HEADLESS = False
SELENIUM_PROXY = "http://user:password@my-proxy-server:port" # set to None to not use a proxy
SELENIUM_USER_AGENT = "User-Agent: Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>"           
SELENIUM_REQUEST_RECORD_SCOPE = ["api*"] # a list of regular expression to record the incoming requests by matching the url
SELENIUM_FIREFOX_PROFILE_SETTINGS = {}
SELENIUM_PAGE_LOAD_TIMEOUT = 120
```








