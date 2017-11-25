# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from tinderspider.items import TinderItem

RESULTS_PER_PAGE = 25

def get_tinder_result_url(page):
    return "https://www.reddit.com/r/Tinder/top/?sort=top&t=all&count=%d" % (page * RESULTS_PER_PAGE)

def is_image_url(url):
    return 'png' in url or 'jpg' in url

page_index = 0
LIMIT = 25

class TinderSpider(scrapy.Spider):
    name = "tinder"
    start_urls = [
        get_tinder_result_url(0)
    ]

    def parse(self, response):
        global page_index
        page_index += 1
        if page_index > LIMIT:
            print('exiting')
            self.skip_item()
        print('scraping page #%d' % page_index)
        things = response.xpath('//div[contains(@class, "thing")]')
        titles = response.xpath('//a[contains(@class, "title may-blank outbound")]/text()').extract()
        num_titles = len(titles)
        items = []
        for i, thing in enumerate(things):
            item = TinderItem()
               
            urls = thing.xpath('@data-url')
            if urls:
                url = urls.extract()[0]
                if is_image_url(url):
                    item['url'] = url
                else:
                    print('not image url', url, 'skipping')
                    continue

            urls = thing.xpath('@data-permalink')
            if urls:
                urls = urls.extract()[0]
                item['permalink'] = url

            if i < num_titles:
                item['title'] = titles[i]
                print(i, item['title'], item['url'])
               
            urls = thing.xpath('@data-author')
            if urls:
                urls = urls.extract()[0]
                item['author'] = urls

             urls = thing.xpath('@data-timestamp')
            if urls:
                urls = urls.extract()[0]
                item['timestamp'] = urls
        
            urls = thing.xpath('@data-comments-count')
            if urls:
                urls = urls.extract()[0] # ex: 91 comments
                item['comments'] = int(urls)
        
            urls = thing.xpath('@data-score')
            if urls:
                urls = urls.extract()[0]
                item['score'] = int(urls)
 
            items.append(item)

        next_page = response.xpath('//span[contains(@class, "next-button")]/a/@href')
        if next_page:
            next_page = next_page.extract()[0]
            next_request = scrapy.Request(next_page, callback = self.parse)
            items.append(next_request)
        yield from items

    # def extract_tinder_items(self, currencies):
        # return [scrapy.Request("%s%s" % (BASE_URL, c), callback=self.parse_currencies, dont_filter=True)
        #         for c in currencies]

    def skip_item(self):
        raise StopIteration

    def parse_tinder(self, response):
        return

