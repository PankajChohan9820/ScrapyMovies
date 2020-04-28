import scrapy
# import Request
from ..items import DemoItem

class MainSpider(scrapy.Spider):
    name = "imdb"
    start_urls = ['https://www.imdb.com/list/ls053327568/']

    def parse(self, response):
        item = DemoItem()
        k = response.css('.mode-detail')
        m ='https://www.imdb.com'
        for movie in k:
            
            item['title'] = movie.css('.lister-item-header a::text').extract_first()
            item['year'] = movie.css('.text-muted.unbold::text').extract_first()
            item['ratings'] = movie.css('.ipl-rating-star.small .ipl-rating-star__rating::text').extract_first()
            urls = movie.css('.lister-item-header a::attr(href)').extract_first()
            final_url = m+urls
            new_item = item.copy()
            print(item)
            yield scrapy.Request(
                url=final_url,
                meta={'item': new_item},
                callback=self.get_data
            )
    

    def get_data(self, response):
        item = response.meta['item']
        item['images_url'] = response.css('.poster img::attr(src)').extract_first(default='').strip()
        stars = response.css('.credit_summary_item~ .credit_summary_item+ .credit_summary_item a::text').extract()[0:3]
        item['stars'] = ','.join(stars)
        print("HelloItem",item)
        print("done")
        yield item