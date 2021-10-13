from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from practice_one.spiders.quotes_spider import QuotesSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(QuotesSpider)
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
settings.set('FEED_FORMAT', 'json')
settings.set('FEED_URI', 'quotes.json')
#process = CrawlerProcess({
#'FEED_FORMAT': 'json',
#'FEED_URI': 'quotes.json'
#})
process.start()
