import scrapy
import csv

class HrefSpider(scrapy.Spider):
    name = "href_spider"
    start_urls = [
        'https://sokoglam.com/collections/skincare'
    ]

    def parse(self, response):
        with open('urls.csv', 'a') as f:
            for link in response.css("h2.product__title a").xpath("@href"):
                href = "https://sokoglam.com" + link.get()
                yield {
                    'href': href
                }

                writer = csv.writer(f)
                writer.writerow([href])

        