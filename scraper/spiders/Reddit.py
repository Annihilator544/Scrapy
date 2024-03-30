
import scrapy

class RedditInSpider(scrapy.Spider):
    name = "Reddit"
    api_url = 'https://www.reddit.com/r/midjourney/new/' 

    def start_requests(self):
        first_url = self.api_url 
        yield scrapy.Request(url=first_url, callback=self.parse_reddit)

    

    def parse_reddit(self, response):
        
        reddit_item = {}
        images = response.css("img")

        num_images = len(images)
        print("******* Num Images Returned *******")
        print(num_images)
        print('*****')
        
        # num_titles = len(titles)
        # print("******* Num Titles Returned *******")
        # print(num_titles)
        # print('*****')
        
        # for title in titles:
        #     title_text = title.css("::attr(slot)").extract_first()
           
        #     if(title_text != None):
        #         if(title_text.startswith("title")):
        #                 print("******* Title Text *******")
        #                 print(title_text)
        #                 print('*****')
        #                 reddit_item['title'] = title_text
        #                 break
        
        for image in images:
            image_url = image.css("::attr(src)").extract_first()
            if(image_url and image_url.startswith("https://preview.redd.it")):
                reddit_item['image_url'] = image_url
            yield  reddit_item
        if num_images > 0:
            nextReq = response.css('shreddit-post').css('::attr(more-posts-cursor)').extract_first()
            next_url = 'https://www.reddit.com/svc/shreddit/community-more-posts/new/?after='+nextReq+'%3D%3D&t=DAY&name=aiArt&feedLength=300'
            yield scrapy.Request(url=next_url, callback=self.parse_reddit)