import csv
import scrapy
import json
from scrapy import Request

class ExtractDataSpider(scrapy.Spider):
    name = "extract_data"

    def __init__(self):
        self.responses = []
        self.pageNum = 1
    
    def start_requests(self):
        with open('productlist.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                productID = row['product_ID']
                request = Request.from_curl("curl 'https://staticw2.yotpo.com/batch/app_key/kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG/domain_key/10296751369/widget/reviews' -H 'authority: staticw2.yotpo.com' -H 'accept: application/json' -H 'accept-language: en-US,en;q=0.5' -H 'content-type: application/x-www-form-urlencoded' -H 'origin: https://sokoglam.com' -H 'referer: https://sokoglam.com/' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: cross-site' -H 'sec-gpc: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' --data-raw 'methods=%5B%7B%22method%22%3A%22reviews%22%2C%22params%22%3A%7B%22pid%22%3A%22"+str(productID)+"%22%2C%22order_metadata_fields%22%3A%7B%7D%2C%22widget_product_id%22%3A%22"+str(productID)+"%22%2C%22data_source%22%3A%22default%22%2C%22page%22%3A"+str(self.pageNum)+"%2C%22host-widget%22%3A%22main_widget%22%2C%22is_mobile%22%3Afalse%2C%22pictures_per_review%22%3A10%7D%7D%5D&app_key=kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG&is_mobile=false&widget_version=2023-02-13_11-23-53' --compressed", callback=self.parse)
                yield request

    def parse(self, response):
        print("parse function fired!! Page: " + str(self.pageNum))
        # Store the response in a list for later processing
        self.responses.append(response)
        print("Total Pages Crawled: " + str(len(self.responses)))
        # Response Data
        data = json.loads(response.text)
        selector = scrapy.Selector(text=data[0]['result'], type="html")
        productID = selector.xpath("//div[@class='y-label product-link']/@data-product-id").get()
        # Follow pagination
        next_page_exist = selector.xpath('//a[@aria-label="Next Page"]/@aria-disabled').get() == 'false'
        if next_page_exist:
            self.pageNum+=1
            request = Request.from_curl("curl 'https://staticw2.yotpo.com/batch/app_key/kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG/domain_key/10296751369/widget/reviews' -H 'authority: staticw2.yotpo.com' -H 'accept: application/json' -H 'accept-language: en-US,en;q=0.5' -H 'content-type: application/x-www-form-urlencoded' -H 'origin: https://sokoglam.com' -H 'referer: https://sokoglam.com/' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: cross-site' -H 'sec-gpc: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' --data-raw 'methods=%5B%7B%22method%22%3A%22reviews%22%2C%22params%22%3A%7B%22pid%22%3A%22"+str(productID)+"%22%2C%22order_metadata_fields%22%3A%7B%7D%2C%22widget_product_id%22%3A%22"+str(productID)+"%22%2C%22data_source%22%3A%22default%22%2C%22page%22%3A"+str(self.pageNum)+"%2C%22host-widget%22%3A%22main_widget%22%2C%22is_mobile%22%3Afalse%2C%22pictures_per_review%22%3A10%7D%7D%5D&app_key=kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG&is_mobile=false&widget_version=2023-02-13_11-23-53' --compressed", callback=self.parse)
            yield request
        else:
            self.pageNum = 1
        
        
    def closed(self, reason):
        reviews = list(self.parse_reviews())
        with open('productReviews.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reviews[0].keys())
            writer.writeheader()
            writer.writerows(reviews)
            
    def parse_reviews(self):
        for response in self.responses:
            data = json.loads(response.text)
            selector = scrapy.Selector(text=data[0]['result'], type="html")
            # list of reviews
            reviews = selector.xpath("//div[@class='content-review']/text()").getall()
            # product ID
            productID = selector.xpath("//div[@class='y-label product-link']/@data-product-id").get()
            productName = selector.xpath("//div[@class='y-label product-link']/text()").get()
            # List of reviewers
            reviewers = selector.xpath("//span[@class='y-label yotpo-user-name yotpo-font-bold pull-left']/text()").getall()
            # list of skinType + ageRange (i = i+2 two record per person)
            reviewerSkinTypeAndAgeRange = selector.xpath("//span[@class='yotpo-user-field-answer text-s']/text()").getall()
            # list of reviews title
            #reviewTitles = selector.xpath("//div[@class='content-title yotpo-font-bold']/text()").getall()

            if len(reviews) == 0:
                continue

            j=0
            for i in range(len(reviews)):
                if i == 5:
                    break
                if "Hi" in reviews[i] or len(reviews[i]) == 1:
                    continue
                try:
                    yield {
                        'productID' : productID,
                        'productName' : productName,
                        'reviewer' : reviewers[i],
                        'reviewer_skinType' : reviewerSkinTypeAndAgeRange[j],
                        'reviewer_ageRange' : reviewerSkinTypeAndAgeRange[j+1],
                        #'reviewTitles' : reviewTitles[i],
                        'review' : reviews[i]
                    }
                except IndexError:
                    continue
                else:
                    j = j + 4