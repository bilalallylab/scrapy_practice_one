import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from w3lib.html import remove_tags
from scrapy.http.request import Request


class DoordashItems(scrapy.Item):
    restaurant_name = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    address = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    working_hours = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    # price_range = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Identity())
    number_of_ratings = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    average_rating = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    reviews = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    # menu_items = len(scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Identity()))


class DoordashSpider(scrapy.Spider):
    name = 'doordash'
    # main_url = "https://www.doordash.com/"
    # start_urls = ["https://www.doordash.com/"]

    def __init__(self, city="", state="", **kwargs):
        if city and state:
            self.start_urls = ['https://www.doordash.com/food-delivery/{city}-{state}-restaurants/'.format(
                city=city.lower(), state=state.lower())]
        else:
            self.start_urls = ["https://www.doordash.com/"]
            # self.start_urls = ["https://www.doordash.com/food-delivery/austin-tx-restaurants/"]
        super().__init__(**kwargs)

    def parsing(self, response):
        load = ItemLoader(item=DoordashItems(), selector=response)
        load.add_xpath('restaurant_name', '//*[@id="__next"]/div[2]/div[1]/div[1]/div[1]/header/div[2]/h1/text()')
        load.add_xpath('address', '//*[@id="__next"]/div[2]/div[1]/div[1]/div[1]/div[14]/div/div[2]/span[3]/text()')
        load.add_xpath('working_hours', '//*[@id="__next"]/div[2]/div[1]/div[1]/div[1]/div[2]/span/text()')
        load.add_xpath('number_of_ratings',
                       '//*[@id="__next"]/div[2]/div[1]/div[1]/div[1]/header/div[2]/div[1]/div[3]/div/span[2]/text()')
        load.add_xpath('average_rating',
                       '//*[@id="__next"]/div[2]/div[1]/div[1]/div[1]/header/div[2]/div[1]/div[3]/div/span[1]/text()')
        load.add_xpath('reviews', './/div[2]/h2/text()')

        price_range = "{min_price} - {max_price}".format(
            min_price=min(response.xpath('//*[@data-anchor-id="StoreMenuItemPrice"]/text()').getall()),
            max_price=max(response.xpath('//*[@data-anchor-id="StoreMenuItemPrice"]/text()').getall()))
        load.add_value('price_range', price_range)

        menu_items = len(response.xpath('//*[@data-anchor-id="MenuItem"]').getall())
        load.add_value('menu_items', menu_items)

        yield load.load_item()

    def parse(self, response):
        for i in range(len(response.xpath(
                '//*[@id="__next"]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/a'))):
            if 'href' in response.css('.next a').attrib:
                restaurant_page_url = response.xpath(
                    '//*[@id="__next"]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/a[%s]/@href' % i)
                if restaurant_page_url is not None:
                    yield response.follow(restaurant_page_url, callback=self.parsing)

