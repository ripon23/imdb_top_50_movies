import scrapy

class TopMoviesSpider(scrapy.Spider):
    name = 'top_movies'
    start_urls = ['https://www.imdb.com/chart/top']

    def parse(self, response):
        # Extract movie links from the top 50 list
        movie_links = response.css('.titleColumn a::attr(href)').extract()
        for link in movie_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_movie)

    def parse_movie(self, response):
        # Extract movie details
        movie_name = response.css('h1::text').get()
        year = response.css('#titleYear a::text').get()
        director = response.css('h4:contains("Director:") + a::text').get()
        stars = response.css('h4:contains("Stars:") + a::text').extract()

        # Clean up data
        if year:
            year = year.strip('()')
        if director:
            director = director.strip()
        stars = [star.strip() for star in stars]

        self.log(f'Relevant Elements: {movie_name}')
        
        # Yield the extracted data
        yield {
            'movie_name': movie_name,
            'year': year,
            'director': director,
            'stars': stars
        }
