import scrapy


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    
    def start_requests(self):
        yield scrapy.Request('https://www.myntra.com/', meta={'playwright': True})

    def parse(self, response):
        yield{
            'text': response.text
        }
        # products = response.css('product-item')
        # for product in products:
        #     #here we put the data returned into the format we want to output for our csv or json file
        #     yield{
        #         'name' : product.css('a.product-item-meta__title::text').get(),
        #         'price' : product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>',''),
        #         'url' : product.css('div.product-item-meta a').attrib['href'],
        #     }
        # next_page = response.css('[rel="next"] ::attr(href)').get()

        # if next_page is not None:
        #     next_page_url = 'https://www.chocolate.co.uk' + next_page
        #     yield response.follow(next_page_url, callback=self.parse)
