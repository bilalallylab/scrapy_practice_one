import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import betamax
import scrapy
from practice_one.spiders.quotes_spider import QuotesSpider
from practice_one.spiders.quotes_spider import QuotesItem
import os
import json
from scrapy.http import HtmlResponse
from betamax.fixtures.unittest import BetamaxTestCase


CASSETTE_LIBRARY_DIR = 'cassettes_result'
if not os.path.exists(CASSETTE_LIBRARY_DIR):
    os.mkdir(CASSETTE_LIBRARY_DIR)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = CASSETTE_LIBRARY_DIR
    config.preserve_exact_body_bytes = True


class BetamaxTestSpider(CrawlSpider):
    name = 'test'

    def parse_item(self, response):
        sp_obj = QuotesSpider()
        qi_obj = QuotesItem()

        response = self.session.get(sp_obj.start_urls[0])

        scrapy_response = HtmlResponse(body=response.content, url=sp_obj.start_urls[0])

        result = sp_obj.parse(scrapy_response)

        for each_item in result:
            if isinstance(each_item, QuotesItem):
                self.assertEqual(each_item['quote_text'], str)
                self.assertEqual(each_item['author'], str)
                self.assertEqual(each_item['tags'], list)
            else:
                raise ValueError('yield output unexpected item')
