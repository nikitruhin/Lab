import re

class CleanDataPipeline:
    def process_item(self, item, spider):
        for field in item:
            if isinstance(item[field], str):
                item[field] = self.clean_field(item[field])
        return item
    
    def clean_field(self, text):
        if not text:
            return text
        
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\.[a-z\-]+\s*{[^}]*}', '', text)
        
        text = re.sub(r'\[\d+\]', '', text)
        

        text = re.sub(r'[,;]\s+[,;]', ',', text)  
        text = re.sub(r'^\s*[,;]\s*|\s*[,;]\s*$', '', text) 
        

        if re.search(r'\b\d{4}\b', text):
            year_match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
            if year_match:
                text = year_match.group(0)
        

        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()


class ImdbPipeline:
    def process_item(self, item, spider):
        if not item.get('imdb_rating') or item['imdb_rating'] == 'N/A':
            title = item.get('title', '')
            year = item.get('year', '')
            
            if title:
                try:
                    url = f"https://v2.sg.media-imdb.com/suggestion/t/{title.replace(' ', '_')}.json"
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('d') and len(data['d']) > 0:
                            best_match = data['d'][0]
                            item['imdb_rating'] = best_match.get('l', 'N/A')
                            item['imdb_year'] = best_match.get('y', 'N/A')
                            item['imdb_id'] = best_match.get('id', '').replace('tt', '')
                except:
                    pass
        
        return item 