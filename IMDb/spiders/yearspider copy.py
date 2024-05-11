import json

import scrapy
from bs4 import BeautifulSoup

from ..items import IMDbYearItem
from .helpers import catch, digits, unicode


class YearSpider(scrapy.Spider):
    name = "imdb_year22"

    allowed_domains = ["www.imdb.com"]

    page_number = 5

    def __init__(self, title_type=None, year=None, *args, **kwargs):
        #print("============================ Test 1 ==========================")
        if title_type and year is None:
            raise ValueError("Title Type & Year are required")
        #print("============================ Test 2 ==========================")
        super(YearSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
        self.title_type = title_type
        self.year = year
        #print("============================ Test 3 ==========================")

    def parse(self, response):

        print("============================ Start ==========================")
        items = IMDbYearItem()
        
        content_tag = response.css('li.ipc-metadata-list-summary-item').extract()
        #print(content_tag)                

        #content_tag = response.css('h3.ipc-title__text::text').extract()
        #print(content_tag, "------------------")

        # titles = max([digits(tag) for tag in response.css(
        #     'div[class=desc] span::text').get().split(' ') if digits(tag) is not None])
        desc_text = response.css('div.desc span::text').get()
        if desc_text:
            titles = max([digits(tag) for tag in desc_text.split(' ') if digits(tag) is not None])

        print("======= Titals===========", titles)

        total_titles = round(titles / 5) + 2

        total_pages = max(
            [1] + [(num * 5) + 1 for num in range(1, total_titles)])

        soup = BeautifulSoup(response.text, 'lxml')

        cast_crew = soup.find_all('p', class_="")

        for fcc, tag in zip(cast_crew, content_tag):

            items['movie_name'] = tag.css('h3::text').get()
            items['movie_id'] = catch('None', lambda: unicode(
                tag.css('h3[class=lister-item-header] a::attr(href)').get()[7:-16]))
            items['movie_url'] = catch('None', lambda: "%s%s" % (
                'https://www.imdb.com', unicode(tag.css('h3[class=lister-item-header] a::attr(href)').get()[:-16])))
            items['poster'] = unicode(response.css(
                'img[class=loadlate]::attr(src)').get())

            year_value = digits(tag.css('span.lister-item-year::text').get())
            items['year'] = int(str(year_value)[:4]) if len(
                str(year_value)) == 8 else year_value
            items['genre'] = catch('None', lambda: tag.css(
                'p:nth-child(2) > span.genre::text').get().replace(',', ' ').split())
            items['runtime'] = tag.css('span.runtime::text').get()
            items['certificate'] = tag.css('span.certificate::text').get()
            items['rating'] = tag.css(
                'div.ratings-imdb-rating::attr(data-value)').get()
            items['metascore'] = tag.css('span.metascore::text').get()
            items['plot'] = catch('None', lambda: unicode(
                ' '.join(tag.css('p:nth-child(4)::text').get().split())))
            items['votes'] = digits(
                tag.css('p.sort-num_votes-visible > span:nth-child(2)::attr(data-value)').get())
            items['gross'] = tag.css(
                'p.sort-num_votes-visible > span:nth-child(5)::text').get()

            # BeautifulSoup

            if fcc.select_one('span.ghost'):
                director_tag = catch('None', lambda: fcc.select_one(
                    'span').findPreviousSiblings('a'))
                cast_tag = catch('None', lambda:  fcc.select_one(
                    'span').findNextSiblings('a'))

                items['director'] = catch('list', lambda:  [unicode(
                    director.get_text()) for director in director_tag])
                items['director_id'] = catch('list', lambda:  [unicode(
                    director['href'][6:-18]) for director in director_tag])
                items['director_url'] = catch('list', lambda:  ["%s%s" % (
                    'https://www.imdb.com', unicode(director['href'][:-18])) for director in director_tag])
                items['cast'] = catch('list', lambda:  [unicode(
                    cast.get_text()) for cast in cast_tag])
                items['cast_id'] = catch('list', lambda:  [unicode(
                    cast['href'][6:-18]) for cast in cast_tag])
                items['cast_url'] = catch('list', lambda:  ["%s%s" % (
                    'https://www.imdb.com', unicode(cast['href'][:-18])) for cast in cast_tag])

            else:
                items['director'] = []
                items['director_id'] = []
                items['director_url'] = []
                items['cast'] = catch('list', lambda:  [unicode(
                    cast.get_text()) for cast in fcc.select('a')])
                items['cast_id'] = catch('list', lambda:  [unicode(
                    cast['href'][6:-18]) for cast in fcc.select('a')])
                items['cast_url'] = catch('list', lambda:  ["%s%s" % (
                    'https://www.imdb.com', unicode(cast['href'][:-18])) for cast in fcc.select('a')])

            yield items
            self.movie_count = len(items)
            if self.movie_count >= 3:
                self.logger.info("Reached top 10 movies, stopping spider.")
                raise scrapy.exceptions.CloseSpider(reason="Reached top 3 movies")

        # next_page = "https://www.imdb.com/search/title/?title_type=feature&release_date=2020-01-01,2024-12-31&count=5"
        # if YearSpider.page_number <= total_pages:
        #     YearSpider.page_number += 5
        #     yield response.follow(next_page, callback = self.parse)