import scrapy


class CodropsSpider(scrapy.Spider):
    name = "codrops"
    allowed_domains = ["tympanus.net"]
    start_urls = ["https://tympanus.net/codrops/category/playground/"]
    page_count = 1
    def parse(self, response):
        
        for x in range(1, 22):
            next_page_url = 'https://tympanus.net/codrops/category/playground/page/'+str(x)+'/'
            yield response.follow(next_page_url, callback=self.parsed)

    def parsed(self, response):
        products = response.css('div.ct-latest-description h2  a ::attr(href)').getall()
        for product in products:
            #here we put the data returned into the format we want to output for our csv or json fil
            yield response.follow(product, callback=self.parse_detail)
            
    def parse_detail(self, response):
        yield{
            'name' : response.css("div.ct-post h1 ::text").get(),
            'demo': response.css("div.ct-demo-links a ::attr(href)").get(),
            'github': response.css("div.ct-demo-links a ::attr(href)").getall()[1],
        }