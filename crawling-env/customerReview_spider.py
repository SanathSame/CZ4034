import csv
import scrapy
import json
from scrapy import Request
from scrapy.selector import Selector

class ExtractDataSpider(scrapy.Spider):
    name = "extract_data"

    def start_requests(self):
        with open('urls.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                url = row[0]
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.productName = response.css("div.review-stars div").xpath("@data-name").get()
        self.productID = response.css("div.review-stars div").xpath("@data-product-id").get()
        self.brand = response.css("h3.pdp__product-vendor a::text").get()
        self.price = response.css("span.pdp__product-price span::text").get()
      

        method = "methods=%5B%7B%22method%22%3A%22main_widget%22%2C%22params%22%3A%7B%22pid%22%3A%22" + self.productID + "%22%2C%22order_metadata_fields%22%3A%7B%7D%2C%22widget_product_id%22%3A%22" + self.productID + "%22%7D%7D%5D"
        request = Request.from_curl("curl 'https://staticw2.yotpo.com/batch/app_key/kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG/domain_key/6866178441285/widget/main_widget' -H 'authority: staticw2.yotpo.com' -H 'accept: application/json' -H 'accept-language: en-US,en;q=0.8' -H 'content-type: application/x-www-form-urlencoded' -H 'origin: https://sokoglam.com' -H 'referer: https://sokoglam.com/' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: cross-site' -H 'sec-gpc: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' --data-raw '" + method + "&app_key=kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG&is_mobile=false&widget_version=2023-02-08_14-34-00' --compressed", callback=self.parse_dynamic)
        
        #yield scrapy.Request(url=request, callback=self.parse_dynamic)
        yield request

    def parse_dynamic(self, response):

        data = json.loads(response.text)
        selector = scrapy.Selector(text=data[0]['result'], type="html")

        # review count
        reviewCount = int(selector.xpath("//span[@class='reviews-qa-label font-color-gray']/text()").get().split(" ")[0])

        # List of reviewers
        reviewers = selector.xpath("//span[@class='y-label yotpo-user-name yotpo-font-bold pull-left']/text()").getall()
        # list of skinType + ageRange (i = i+2 two record per person)
        reviewerSkinTypeAndAgeRange = selector.xpath("//span[@class='yotpo-user-field-answer text-s']/text()").getall()
        # list of reviews title
        reviewTitles = selector.xpath("//div[@class='content-title yotpo-font-bold']/text()").getall()
        # list of reviews
        reviews = selector.xpath("//div[@class='content-review']/text()").getall()

        
        if reviewCount == 0:
            # Skip the current iteration if the title is empty
            return

        with open("output.csv", "a", newline='') as f:
            j = 0
            for i in range(reviewCount):
                writer = csv.writer(f)
                writer.writerow([self.productID, self.productName, self.brand, self.price, reviewCount, reviewers[i], reviewerSkinTypeAndAgeRange[j], reviewerSkinTypeAndAgeRange[j+1],reviewTitles[i], reviews[i]])
                
            item = {
                'productName': self.productName,
                'productID': self.productID,
                'brand': self.brand,
                'price': self.price,
                'reviewCount': reviewCount,
                'reviewer': reviewers[i],
                'reviewerSkinType': reviewerSkinTypeAndAgeRange[j],
                'reviewerAgeRange': reviewerSkinTypeAndAgeRange[j+1],
                'reviewTitle': reviewTitles[i],
                'reviews': reviews[i]
            }

            j = j + 4
        yield item
                    
            

'''
    def closed(self, reason):
        with open("output.csv", "a", newline='') as f:
            writer = csv.writer(f)
            for item in self.items:
                writer.writerow([item['productName'], item['productID'], item['brand'], item['price'], item['reviewCount'], item['reviewer'], item['reviewerSkinType'], item['reviewerAgeRange'], item['reviewTitle'], item['reviews']])
'''