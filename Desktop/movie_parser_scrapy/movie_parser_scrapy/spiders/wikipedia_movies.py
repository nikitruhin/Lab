import scrapy
from urllib.parse import urljoin
import re
import time

class WikipediaMoviesSpider(scrapy.Spider):
    name = 'wikipedia_movies'
    allowed_domains = ['ru.wikipedia.org', 'imdb.com', 'www.imdb.com']
    start_urls = ['https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 2,
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'movies_with_imdb.csv',
    }
    
    def __init__(self, max_movies=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_movies = int(max_movies)
        self.collected = 0
        self.visited_wiki = set()
        self.visited_imdb = set()
    
    def parse(self, response):
        if response.url in self.visited_wiki:
            return
        
        self.visited_wiki.add(response.url)
        
        movie_elements = response.css('#mw-pages .mw-category-group li a')
        
        for element in movie_elements:
            if self.collected >= self.max_movies:
                return
            
            href = element.attrib.get('href', '')
            text = element.css('::text').get('')
            
            if self.is_valid_movie_link(href, text):
                movie_url = urljoin(response.url, href)
                
                if movie_url not in self.visited_wiki:
                    self.visited_wiki.add(movie_url)
                    yield scrapy.Request(
                        movie_url, 
                        callback=self.parse_movie_wiki,
                        meta={'start_time': time.time()}
                    )
                    self.collected += 1
        
        if self.collected < self.max_movies:
            next_page = self.find_next_category_page(response)
            if next_page and next_page not in self.visited_wiki:
                yield response.follow(next_page, callback=self.parse)
    
    def is_valid_movie_link(self, href, text):
        if not href or not text:
            return False
        
        if ':' in href.split('/wiki/')[-1]:
            return False
        
        exclude_patterns = ['Категория:', 'Файл:', 'Шаблон:', 'Википедия:', 'Обсуждение:']
        if any(pattern in href for pattern in exclude_patterns):
            return False
        
        return True
    
    def find_next_category_page(self, response):
        next_selectors = [
            '//a[contains(text(), "Следующая страница")]/@href',
            '//a[contains(text(), "След.")]/@href',
            'a:contains("Далее")::attr(href)',
        ]
        
        for selector in next_selectors:
            if '::' in selector:
                link = response.css(selector).get()
            else:
                link = response.xpath(selector).get()
            
            if link:
                return urljoin(response.url, link)
        
        return None
    
    def parse_movie_wiki(self, response):
        start_time = response.meta.get('start_time', time.time())
        
        title = self.clean_text(
            response.css('h1#firstHeading span::text').get() or 
            response.css('h1#firstHeading::text').get() or 
            response.css('h1::text').get()
        )
        
        def get_table_data(labels):
            for label in labels:
                xpath = f'//table[contains(@class, "infobox")]//tr[th[contains(., "{label}")]]/td//text()'
                data = response.xpath(xpath).getall()
                if data:
                    cleaned = [self.clean_text(d) for d in data if d and not d.strip().startswith('[')]
                    return ', '.join(cleaned) if cleaned else None
            return None
        
        genre = get_table_data(['Жанр', 'Жанры'])
        director = get_table_data(['Режиссёр', 'Режиссер', 'Режиссёры'])
        country = get_table_data(['Страна', 'Страны'])
        year = get_table_data(['Год', 'Дата выхода'])
        
        if not year or year == 'N/A':
            year_match = re.search(r'\((\d{4})\)', title)
            if year_match:
                year = year_match.group(1)
            else:
                first_para = response.css('.mw-parser-output p::text').get()
                if first_para:
                    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', first_para)
                    year = year_match.group(0) if year_match else 'N/A'
        
        item = {
            'title': title,
            'year': year or 'N/A',
            'genre': genre or 'N/A',
            'director': director or 'N/A',
            'country': country or 'N/A',
            'url_wiki': response.url,
            'imdb_url': '',
            'imdb_rating': 'Не найден',
        }
        
        imdb_url = response.xpath('//a[contains(@href, "imdb.com/title/tt")]/@href').get()
        
        if imdb_url:
            if not imdb_url.startswith('http'):
                imdb_url = f'https://www.imdb.com{imdb_url}' if imdb_url.startswith('/') else f'https://{imdb_url}'
            
            request_meta = {
                'item': item,
                'start_time': start_time,
                'dont_redirect': True,
                'handle_httpstatus_list': [301, 302],
            }
            
            yield scrapy.Request(
                url=imdb_url,
                callback=self.parse_imdb,
                meta=request_meta,
                dont_filter=True
            )
        else:
            item['parse_time'] = round(time.time() - start_time, 2)
            yield item
    
    def parse_imdb(self, response):
        item = response.meta['item']
        start_time = response.meta.get('start_time', time.time())
        
        rating = response.css('div[data-testid="hero-rating-bar__aggregate-rating__score"] span::text').get()
        
        if not rating:
            rating = response.css('span[itemprop="ratingValue"]::text').get()
        
        if not rating:
            rating = response.css('div.imdbRating span.rating span::text').get()
        
        if rating:
            rating = self.clean_text(rating)
        
        imdb_year = response.css('a[href*="releaseinfo"]::text').get()
        if not imdb_year:
            imdb_year = response.css('span.TitleBlockMetaData__ListItemText-sc-12ein40-2::text').get()
        
        item.update({
            'imdb_url': response.url,
            'imdb_rating': rating or 'Нет оценки',
            'imdb_year': self.clean_text(imdb_year) if imdb_year else '',
            'parse_time': round(time.time() - start_time, 2),
        })
        
        yield item
    
    def clean_text(self, text):
        if not text:
            return ''
        
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\[\d+\]', '', text)
        return text