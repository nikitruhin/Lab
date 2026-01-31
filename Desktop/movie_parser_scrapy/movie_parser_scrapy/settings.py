BOT_NAME = 'movie_parser_scrapy'
SPIDER_MODULES = ['movie_parser_scrapy.spiders']
NEWSPIDER_MODULE = 'movie_parser_scrapy.spiders'

ROBOTSTXT_OBEY = False
USER_AGENT = 'Mozilla/5.0'
DOWNLOAD_DELAY = 0.7
CONCURRENT_REQUESTS = 1

ITEM_PIPELINES = {
    'movie_parser_scrapy.pipelines.CleanDataPipeline': 100,  
    'movie_parser_scrapy.pipelines.ImdbPipeline': 300,       
}
