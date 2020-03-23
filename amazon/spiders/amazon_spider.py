import scrapy
from ..items import AmazonItem 

class AmazonSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = [
        'https://www.amazon.in/s?rh=n%3A1968094031%2Cp_72%3A4-&pf_rd_i=1968094031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=967e38e4-edd0-5851-8733-35708778cfba&pf_rd_r=05NEHJ3PH9KPD45P4NT1&pf_rd_s=merchandised-search-5&pf_rd_t=101&ref=Oct_TopRatedC_1968094031_SAll'
        ]
    count = 0
    LIMIT = 1000    

    def parse(self, response):
        item = AmazonItem()
        h2s = response.css('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2')
        for h2 in h2s:
            link = h2.css('a.a-link-normal.a-text-normal::attr(href)').extract_first() #.get()
            if not link.startswith('/gp/slredirect'):
                print("yes")
                item['link'] = link
                if self.count>=60:
                    break
                self.count = self.count + 1;
                yield  item
        # print(links)
        print(self.count)
        next_page = response.css('li.a-last a::attr(href)').extract_first()

        if self.count<60:
            yield  response.follow(next_page, callback=self.parse)  
    
    def scrap_product(self, response, args):
        pass
