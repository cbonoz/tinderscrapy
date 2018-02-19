# tinderscrapy
Tinder conversation scraper written in python.
- scrapy
- tessaract

## How to run:
2 steps:<br/>

* Run the spider to produce tinder reddit post information out in tinder_{timestamp}.csv: <pre>scrapy crawl tinder</pre>
* Run tinder_processor.py to fetch the image files from the reddit posts in tinder.csv and output the processed image text content into conversations.csv.
