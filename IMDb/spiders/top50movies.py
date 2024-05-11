import scrapy
from scrapy import Selector

class IMDBSpider(scrapy.Spider):
    name = 'imdb_topmovies'

    def start_requests(self):        
        # Start the scraping process by sending a request to IMDb's top movies page
        yield scrapy.Request("https://www.imdb.com/chart/top/?ref_=nv_mv_250", callback=self.parse)
        
    def parse(self, response):
        # Extracting links of the top 50 movies from the IMDb chart
        links = response.css('div.cli-title > a.ipc-title-link-wrapper::attr(href)').extract()
        links_first_50 = links[:50]
        for link in links_first_50:
            # Follow each movie link and call parse_movie_detail_page function for further processing
            yield response.follow(link, callback=self.parse_movie_detail_page)               
    
    def parse_movie_detail_page(self, response):
        data = {}
        
        # Extracting movie name
        data['name'] = response.css('h1[data-testid="hero__pageTitle"] span[data-testid="hero__primary-text"]::text').get()                                
        
        # Extracting year of release
        data['year_of_release'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a/text()').get()

        # Extracting director's name
        data['director'] = response.xpath('//li[contains(@data-testid, "title-pc-principal-credit")][1]//a[contains(@href, "/name/")]/text()').get()
        
        # Extracting stars' names
        stars_parent_element = response.xpath('//a[contains(text(), "Stars")]/parent::li').extract_first()        
        stars_parent_selector = Selector(text=stars_parent_element)
        data['stars'] = ', '.join(stars_parent_selector.xpath('.//a[contains(@class, "ipc-metadata-list-item__list-content-item--link")]/text()').extract())         
        
        # Logging the extracted movie details
        self.log(f'Movie Elements: {data}')      
        
        # Yielding the extracted data
        yield data
