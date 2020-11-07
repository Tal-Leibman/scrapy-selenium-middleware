# scrapy-selenium-middleware

## requirements
* This downloader middleware should be used inside an existing [Scrapy](https://scrapy.org/) project
* Install  Firefox and [gekodriver](https://github.com/mozilla/geckodriver/releases) on the machine running this middleware

## pip
* `pip install`
 
## usage example
The middleware receives its settings from scrapy project settings<br>

in your scrapy project settings.py file add the following settings
~~~python~~~
DOWNLOADER_MIDDLEWARES = {"scrapy_selenium_middleware.SeleniumDownloader":451}
CONCURRENT_REQUESTS = 1 # multiple concurrent browsers are not supported yet
SELENIUM_IS_HEADLESS = False
SELENIUM_PROXY = "http://user:password@my-proxy-server:port" # set to None to not use a proxy
SELENIUM_USER_AGENT = "User-Agent: Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>"           
SELENIUM_REQUEST_RECORD_SCOPE = ["api*"] # a list of regular expression to record the incoming requests by matching the url
SELENIUM_FIREFOX_PROFILE_SETTINGS = {}
~~~








