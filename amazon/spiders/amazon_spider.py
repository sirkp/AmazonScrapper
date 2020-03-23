import scrapy
from ..items import AmazonItem 

class AmazonSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = [
        'https://www.amazon.in/s?rh=n%3A1968094031%2Cp_72%3A4-&pf_rd_i=1968094031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=967e38e4-edd0-5851-8733-35708778cfba&pf_rd_r=05NEHJ3PH9KPD45P4NT1&pf_rd_s=merchandised-search-5&pf_rd_t=101&ref=Oct_TopRatedC_1968094031_SAll'
        ]
    item_limit = 1000
    page_number = 2
    count = 0
    page_limit = 40    

    def parse(self, response):
        divs = response.css('div.a-section.a-spacing-medium.a-text-center')
        print("div thik- ",len(divs))
        temp =0


        for div in divs:
            link = div.css('a.a-link-normal.a-text-normal::attr(href)').extract_first() #.get()
            print('got link')
            if not link.startswith('/gp/slredirect'):
                print("inside loop")
                
                base_price_with_symbol = div.css('.a-text-price span::text').extract_first() # ye ni ho skta hai
                if base_price_with_symbol is not None:
                    base_price = base_price_with_symbol[1:len(base_price_with_symbol)]
                print('base_price')
                
                final_price = div.css('.a-price-whole::text').extract_first()
                print('got final_price')
                
                if base_price is None:
                    base_price = final_price
                
                discount_with_symbol = div.css('.a-letter-space+ span::text').extract_first()
                if discount_with_symbol is not None:
                    discount = discount_with_symbol.split()[1][1:len(discount_with_symbol)]
                print('got discount')
               
                temp = temp + 1
                print('incremented temp')
                item_detail = {
                    'link': link,
                    'base_price':base_price,
                    'final_price':final_price,
                    'discount':discount
                }
                yield response.follow(link, callback=self.scrap_product, cb_kwargs=dict(item_detail=item_detail))


        print('done yielding')
        print(self.page_number)
        
        # next pagination
        print("prodesses page ",temp)
        next_page = "https://www.amazon.in/s?i=apparel&rh=n%3A1968094031%2Cp_72%3A1318476031&page="+ str(self.page_number) + "&pf_rd_i=1968094031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=967e38e4-edd0-5851-8733-35708778cfba&pf_rd_r=05NEHJ3PH9KPD45P4NT1&pf_rd_s=merchandised-search-5&pf_rd_t=101&qid=1584930567&ref=sr_pg_1"
        if self.page_number<self.page_limit:
            self.page_number = self.page_number + 1
            yield  response.follow(next_page, callback=self.parse)  
    
    def scrap_product(self, response, item_detail):
        if (self.count < self.item_limit):
            item = AmazonItem()
            
            
            product_name = response.css('#productTitle::text').extract_first()
            if product_name is not None:
                product_name = product_name.strip()
            
            brand = response.css(".a-row #bylineInfo::text").extract_first()
            
            rating = response.css('.a-icon.a-icon-star.a-star-4 span::text').extract_first()
            if rating is not None:
                rating = rating.strip()
            
            fit = response.css('#feature-bullets li:nth-child(1) .a-list-item::text').extract_first()
            if fit is not None:
                fit = fit.strip().split(':')[1]

            
            colour = response.css('.selection::text').extract_first()
            if colour is not None:
                colour = colour.strip()
            
            product_details = {} 
            if(len(response.css('#detail_bullets_id li').extract())==6):
                product_details = {
                    'item_part_number': response.css('.content > ul li:nth-child(1)::text').extract_first().strip(),
                    'ASIN': response.css('#detail_bullets_id li:nth-child(2)::text').extract_first().strip(),
                    'date_first_available': response.css('#detail_bullets_id li:nth-child(3)::text').extract_first().strip(),
                    'amazon_bestseller_rank': "".join(response.css('#SalesRank::text').extract()).replace('\n','').replace('#','').replace('(','').replace(')','').strip()
                }
            elif(len(response.css('#detail_bullets_id li').extract())==5):
                product_details = {
                    'item_part_number': None,
                    'ASIN': response.css('#detail_bullets_id li:nth-child(1)::text').extract_first().strip(),
                    'date_first_available': response.css('#detail_bullets_id li:nth-child(2)::text').extract_first().strip(),
                    'amazon_bestseller_rank': "".join(response.css('#SalesRank::text').extract()).replace('\n','').replace('#','').replace('(','').replace(')','').strip()
                }
            elif(len(response.css('#detail_bullets_id li').extract())==3):
                print('3 aaya bhosdik')
                product_details = {
                    'item_part_number': None,
                    'ASIN': response.css('#detail_bullets_id li:nth-child(1)::text').extract_first().strip(),
                    'date_first_available': response.css('#detail_bullets_id li:nth-child(2)::text').extract_first().strip(),
                    'amazon_bestseller_rank': None
                }
            else:
                product_details = {
                    'item_part_number': response.css('.content > ul li:nth-child(2)::text').extract_first().strip(),
                    'ASIN': response.css('#detail_bullets_id li:nth-child(3)::text').extract_first().strip(),
                    'date_first_available': response.css('#detail_bullets_id li:nth-child(4)::text').extract_first().strip(),
                    'amazon_bestseller_rank': "".join(response.css('#SalesRank::text').extract()).replace('\n','').replace('#','').replace('(','').replace(')','').strip()
                }        
                
            item['product_details'] = product_details  
            item['brand'] = brand  
            item['product_name'] = product_name  
            item['rating'] = rating  
            item['fit'] = fit  
            item['colour'] = colour  
            item['link'] = item_detail['link']
            item['base_price'] = item_detail['base_price']
            item['final_price'] = item_detail['final_price']
            item['discount'] = item_detail['discount']
            
            if ((brand is not None) and (product_name is not None)):
                yield  item
                self.count += 1
        
