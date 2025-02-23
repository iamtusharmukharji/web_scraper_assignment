import scrapy
import re

class CrawlerSpider(scrapy.Spider):
    name = "assignment_spider"
    
    def __init__(self, domains=None, *args, **kwargs):
        super(CrawlerSpider, self).__init__(*args, **kwargs)
        
        self.start_urls = [f"https://{domain}" for domain in domains.split(",")]

    
    def parse(self, response):
        """Extract links and print them for debugging"""
        links = response.css("a::attr(href)").getall()
        
        for link in links:
            absolute_url = response.urljoin(link)
            
            # Check for product URLs
            if re.search(r"/(product|itm|p|b)/", absolute_url):
                yield {"product_url": absolute_url}

            # Limit depth to prevent infinite crawling
            elif absolute_url.startswith(response.url) and response.meta.get("depth", 0) < 2:
                yield scrapy.Request(absolute_url, callback=self.parse, meta={"depth": response.meta.get("depth", 0) + 1})
