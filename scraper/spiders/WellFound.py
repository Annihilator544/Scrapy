import scrapy
from urllib.parse import urlencode


class WellfoundSpider(scrapy.Spider):
    name = "WellFound"
    allowed_domains = ["wellfound.com"]
    start_urls = ["https://wellfound.com/jobs"]

    def parse(self, response):
        pass
