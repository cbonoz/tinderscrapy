# tinderscrapy
Tinder conversation scraper written in python.
- scrapy
- tessaract

## How to run:
2 steps:<br/>

* Run the spider to produce tinder reddit post information out in tinder.csv: <pre>scrapy crawl tinder</pre>
* Run process_images.py to fetch the image files from the reddit posts in tinder.csv and output the processed image text content into conversations.csv.
