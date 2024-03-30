import scrapy


class AniwatchspiderSpider(scrapy.Spider):
    name = "AniWatchSpider"
    allowed_domains = ["aniwatchtv.to"]
    start_urls = ["https://aniwatchtv.to/az-list"]

    def parse(self, response):
        products = response.css('div.flw-item')
        for product in products:
            #here we put the data returned into the format we want to output for our csv or json file
            detail ='https://aniwatchtv.to'+ product.css('a.film-poster-ahref ::attr(href)').get()
            yield response.follow(detail, callback=self.parse_detail)
        next_page = response.css('[title="Next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://aniwatchtv.to' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    
    def parse_detail(self, response):
        lists=response.css('span.name ::text').getall()
        listschecker=response.css('span.item-head ::text').getall()
        if(len(lists)!=7):
            if(listschecker[0]!='Japanese:'):
                lists.insert(0,'NULL')    
            if(listschecker[1]!='Synonyms:'):
                lists.insert(1,'NULL')
            if(listschecker[2]!='Aired:'):
                lists.insert(2,'NULL')
            if(listschecker[3]!='Premiered:'):
                lists.insert(3,'NULL')
            if(listschecker[4]!='Duration:'):
                lists.insert(4,'NULL')
            if(listschecker[5]!='Status:'):
                lists.insert(5,'NULL')
            if(listschecker[6]!='MAL Score:'):
                lists.insert(6,'NULL')
        list2=response.css('div.item.item-title a ::text').getall()
        list3=list2.pop(0)
        yield{
            'name' : response.css('h2.film-name ::text').get(),
            'Watch Link':'https://aniwatchtv.to/'+response.css('div.film-buttons a').attrib['href'],
            'image':response.css('img.film-poster-img  ::attr(src)').get(),
            'episodes': response.css('div.tick-sub  ::text').get(),
            'rating': response.css('div.tick-item::text').get(),
            'description': response.css('div.text ::text').get(),
            'japanese': lists[0],
            'Synonyms': lists[1].split(','),
            'Aired': lists[2],
            'Premiered': lists[3],
            'Duration': lists[4],
            'Status': lists[5],
            'MAL Score': lists[6],
            'Genres':response.css('div.item.item-list a ::text').getall(),
            'Studio':list2[0],
            'Producer':list3,
            'Characters&VoiceActors':response.css('h4.pi-name ::text').getall(),
        }
