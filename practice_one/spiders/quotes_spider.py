import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from w3lib.html import remove_tags


class QuotesItem(scrapy.Item):
    quote_text = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    author = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Identity()
    )


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            load = ItemLoader(item=QuotesItem(), selector=quote)
            load.add_xpath('quote_text', './/span/text()')
            load.add_xpath('author', './/span[2]/small/text()')
            load.add_xpath('tags', './/div/a/text()')

            yield load.load_item()

        if 'href' in response.css('.next a').attrib:
            next_page = response.css('.next a').attrib['href']
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

