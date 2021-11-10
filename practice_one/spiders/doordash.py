import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from w3lib.html import remove_tags


class DoordashItems(scrapy.Item):
    restaurant_name = ''
    address = ''
    working_hours = ''
    price_range = ''
    number_of_ratings = ''
    average_rating = ''
    reviews = ''
    menu_items = 0


class DoordashSpider(scrapy.Spider):
    name = 'doordash'
    main_url = "https://www.doordash.com/"

    def __init__(self, city="", state=""):
        if city and state:
            self.start_urls = ['https://www.doordash.com/food-delivery/{city}-{state}-restaurants/'.format(
                city=city.lower(), state=state.lower())]
        else:
            self.start_urls = ["https://www.doordash.com/"]

    def open_res_link(self, res_link):
        yield scrapy.Request("https://www.doordash.com/{res_link}".format(res_link=res_link))

    def parsing(self, response):
        yield {
            'res_name': response.xpath('//*[@class="sc-cMljjf eTbdzc sc-ccLTTT jiSDoO"]/text()').get()
        }

    def parse(self, response):
        yield response
        # for restaurant in response.xpath('//div[@class="sc-gIjDWZ dTAMaS sc-ipZHIp fmFNqT"]/@href'):
        #     response.follow(self.main_url+restaurant, callback=self.parsing)
            # response.xpath("")

            # load = ItemLoader(item=DoordashItems(), selector=restaurant)
            # load.add_xpath('restaurant_name', './/span/text()')
            # load.add_xpath('author', './/span[2]/small/text()')
            # load.add_xpath('tags', './/div/a/text()')
            # yield load.load_item()
