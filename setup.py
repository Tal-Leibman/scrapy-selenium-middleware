from setuptools import setup, find_packages

with open("README.md") as readme_file:
    README = readme_file.read()

setup_args = dict(
    author="Tal Leibman",
    author_email="leibman2@gmail.com",
    url="https://github.com/Tal-Leibman/scrapy-selenium-middleware",
    name="scrapy_selenium_middleware",
    version="0.0.5",
    description="""Scrapy middleware for downloading a page html source using selenium,
                and interacting with the web driver in the request context
                eventually returning an HtmlResponse to the spider
                """,
    long_description=README,
    keywords=[
        "scrapy",
        "selenium",
        "middleware",
        "proxy",
        "web scraping",
        "render javascript",
        "selenium-wire",
        "headless browser",
    ],
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
install_requires = [
    "scrapy==2.4.0",
    "selenium-wire==2.1.1",
    "selenium==3.141.0",
]
if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
