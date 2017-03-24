# -*- coding: utf-8 -*-
import scrapy


class RamenSpider(scrapy.Spider):
    name = "ramen"
    start_urls = ['https://tabelog.com/rstLst/?vs=1&sa=&sk=%25E3%2583%25A9%25E3%2583%25BC%25E3%2583%25A1%25E3%2583%25B3&lid=hd_search1&vac_net=&svd=20170316&svt=1900&svps=2&hfc=1&Cat=MC&sw=']

    def parse(self, response):

        for href in response.css('a.list-rst__rst-name-target::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_single)

        next_page = response.css('a.page-move__target--next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_single(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
                'name': extract_with_css('h2.display-name span::text'),
                'score': extract_with_css('b.rdheader-rating__score-val span::text'),
                'desc': extract_with_css('div.pr-comment span#pr-comment-body::text'),
                }

