import scrapy


class MyntraSpider(scrapy.Spider):
    name = "Myntra"
    allowed_domains = ["www.myntra.com"]
    start_urls = ["https://www.myntra.com/"]

    def parse(self, response):
        Category = response.css("div.desktop-navLink a ::attr(href)").getall()
        for cat in Category:
            yield response.follow('https://www.myntra.com/'+cat, callback=self.parse_category)
    
    def parse_category(self, response):
        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url =  next_page
            yield response.follow(next_page_url, callback=self.parse_pages)   

    def parse_pages(self, response):
        products = response.css('li.product-base')
        for product in products:
            #here we put the data returned into the format we want to output for our csv or json file
            yield{
                'name' : product.css('div.product-productMetaInfo h3.product-brand ::text').get(),
                'price' : product.css('div.product-productMetaInfo div.product-price ::text').get(),
                'url' : product.css('a.product-base ::attr(href)').get(),
            }