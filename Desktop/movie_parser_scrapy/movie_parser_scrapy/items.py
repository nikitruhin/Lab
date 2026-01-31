import scrapy

class MovieItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    genre = scrapy.Field()
    director = scrapy.Field()
    country = scrapy.Field()
    duration = scrapy.Field()
    url = scrapy.Field()
    
    imdb_id = scrapy.Field()
    imdb_rating = scrapy.Field()
    imdb_votes = scrapy.Field()
    imdb_year = scrapy.Field()
    imdb_metascore = scrapy.Field()
    search_accuracy = scrapy.Field()