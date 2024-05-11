import scrapy
from scrapy import Selector
from ..items import IMDbYearItem
class IMDBSpider(scrapy.Spider):
    name = 'imdb_topmovies'

    def start_requests(self):        
        yield scrapy.Request("https://www.imdb.com/chart/top/?ref_=nv_mv_250", callback=self.parse)
        
    def parse(self, response):
        links = response.css('div.cli-title > a.ipc-title-link-wrapper::attr(href)').extract()
        links_first_50 = links[:50]
        for link in links_first_50:
            yield response.follow(link, callback=self.parse_movie_detail_page)               
    
    def parse_movie_detail_page(self, response):
        data = {}
        
        data['name'] = response.css('h1[data-testid="hero__pageTitle"] span[data-testid="hero__primary-text"]::text').get()
        data['director'] = response.xpath('//li[contains(@data-testid, "title-pc-principal-credit")][1]//a[contains(@href, "/name/")]/text()').get()                
        data['year_of_release'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a/text()').get()        
        stars_parent_element = response.xpath('//a[contains(text(), "Stars")]/parent::li').extract_first()        
        stars_parent_selector = Selector(text=stars_parent_element)
        data['stars'] = stars_string = ', '.join(stars_parent_selector.xpath('.//a[contains(@class, "ipc-metadata-list-item__list-content-item--link")]/text()').extract())         
        self.log(f'Relevant Elements: {data}')      
        yield data