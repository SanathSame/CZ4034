import csv
import scrapy
import json
from scrapy import Request


class ExtractDataSpider(scrapy.Spider):
    name = "extract_data"

    def __init__(self):
        self.responses = []
        self.skipRecords = 0
        self.productID = ''
        self.productCount = 0
        self.currentProductName = ''
        self.previousPage = 1

    def start_requests(self):
        startPage = 1
        with open('productlist.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.productCount += 1
                self.productID = row['product_ID']
                self.currentProductName = row['product_name']
                request = Request.from_curl("curl 'https://staticw2.yotpo.com/batch/app_key/kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG/domain_key/10296751369/widget/reviews' -H 'authority: staticw2.yotpo.com' -H 'accept: application/json' -H 'accept-language: en-US,en;q=0.5' -H 'content-type: application/x-www-form-urlencoded' -H 'origin: https://sokoglam.com' -H 'referer: https://sokoglam.com/' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: cross-site' -H 'sec-gpc: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' --data-raw 'methods=%5B%7B%22method%22%3A%22reviews%22%2C%22params%22%3A%7B%22pid%22%3A%22"+str(
                    self.productID)+"%22%2C%22order_metadata_fields%22%3A%7B%7D%2C%22widget_product_id%22%3A%22"+str(self.productID)+"%22%2C%22data_source%22%3A%22default%22%2C%22page%22%3A"+str(startPage)+"%2C%22host-widget%22%3A%22main_widget%22%2C%22is_mobile%22%3Afalse%2C%22pictures_per_review%22%3A10%7D%7D%5D&app_key=kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG&is_mobile=false&widget_version=2023-02-13_11-23-53' --compressed", callback=self.parse, dont_filter=True)
                yield request

    def parse(self, response):
        # Response Data
        data = json.loads(response.text)
        selector = scrapy.Selector(text=data[0]['result'], type="html")
        reviews = selector.xpath(
            "//div[@class='content-review']/text()").getall()
        totalReviews = int(selector.xpath(
            "//div[@class='total-reviews-search']/@total-reviews-search").get())

        # Check for Next Page
        if len(reviews) == 0:
            return

        if len(reviews) == 5:
            currentPage = selector.xpath(
                '//a[@aria-current="true"]/@data-page').get()

            try:
                nextPage = int(currentPage) + 1
            except TypeError:
                if totalReviews > 5:
                    nextPage = self.previousPage + 1
                    request = Request.from_curl("curl 'https://staticw2.yotpo.com/batch/app_key/kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG/domain_key/10296751369/widget/reviews' -H 'authority: staticw2.yotpo.com' -H 'accept: application/json' -H 'accept-language: en-US,en;q=0.5' -H 'content-type: application/x-www-form-urlencoded' -H 'origin: https://sokoglam.com' -H 'referer: https://sokoglam.com/' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: cross-site' -H 'sec-gpc: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' --data-raw 'methods=%5B%7B%22method%22%3A%22reviews%22%2C%22params%22%3A%7B%22pid%22%3A%22"+str(
                        self.productID)+"%22%2C%22order_metadata_fields%22%3A%7B%7D%2C%22widget_product_id%22%3A%22"+str(self.productID)+"%22%2C%22data_source%22%3A%22default%22%2C%22page%22%3A"+str(nextPage)+"%2C%22host-widget%22%3A%22main_widget%22%2C%22is_mobile%22%3Afalse%2C%22pictures_per_review%22%3A10%7D%7D%5D&app_key=kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG&is_mobile=false&widget_version=2023-02-13_11-23-53' --compressed", callback=self.parse, dont_filter=True)
                    yield request
                else:
                    # Store the response in a list for later processing
                    self.responses.append(response)
                    return
            else:
                # Store the response in a list for later processing
                self.responses.append(response)
                self.previousPage = int(currentPage)
                next_page_exist = selector.xpath(
                    '//a[@aria-label="Next Page"]/@aria-disabled').get() == 'false'

                # DEBUG MESSAGES
                print("Total Pages Crawled: " + str(len(self.responses)))
                print("Total Products Crawled: " + str(self.productCount))
                print("Current Product: " + str(self.currentProductName))
                print("Current Page: " + str(currentPage))

                if next_page_exist:
                    request = Request.from_curl("curl 'https://staticw2.yotpo.com/batch/app_key/kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG/domain_key/10296751369/widget/reviews' -H 'authority: staticw2.yotpo.com' -H 'accept: application/json' -H 'accept-language: en-US,en;q=0.5' -H 'content-type: application/x-www-form-urlencoded' -H 'origin: https://sokoglam.com' -H 'referer: https://sokoglam.com/' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: cross-site' -H 'sec-gpc: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' --data-raw 'methods=%5B%7B%22method%22%3A%22reviews%22%2C%22params%22%3A%7B%22pid%22%3A%22"+str(
                        self.productID)+"%22%2C%22order_metadata_fields%22%3A%7B%7D%2C%22widget_product_id%22%3A%22"+str(self.productID)+"%22%2C%22data_source%22%3A%22default%22%2C%22page%22%3A"+str(nextPage)+"%2C%22host-widget%22%3A%22main_widget%22%2C%22is_mobile%22%3Afalse%2C%22pictures_per_review%22%3A10%7D%7D%5D&app_key=kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG&is_mobile=false&widget_version=2023-02-13_11-23-53' --compressed", callback=self.parse, dont_filter=True)
                    yield request
        else:
            # Store the response in a list for later processing
            self.responses.append(response)
            return

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
            reviews = selector.xpath(
                "//div[@class='content-review']/text()").getall()
            # product ID
            productID = selector.xpath(
                "//div[@class='y-label product-link']/@data-product-id").get()
            productName = selector.xpath(
                "//div[@class='y-label product-link']/text()").get()
            # List of reviewers
            reviewers = selector.xpath(
                "//span[@class='y-label yotpo-user-name yotpo-font-bold pull-left']/text()").getall()
            # list of skinType + ageRange (i = i+2 two record per person)
            reviewerSkinTypeAndAgeRange = selector.xpath(
                "//span[@class='yotpo-user-field-answer text-s']/text()").getall()
            # list of reviews title
            reviewTitles = selector.xpath(
                "//div[@class='content-title yotpo-font-bold']/text()").getall()
            # Rating stars
            # ratingStars = selector.xpath("//span[@class='sr-only']/text()").getall()

            if len(reviews) == 0:
                continue

            j = 0
            for i in range(len(reviews)):
                if i == 5:
                    break
                if "Hi" in reviews[i] or len(reviews[i]) == 1:
                    continue
                try:
                    yield {
                        'productID': productID,
                        'productName': productName,
                        'reviewer': reviewers[i],
                        'reviewer_skinType': reviewerSkinTypeAndAgeRange[j],
                        'reviewer_ageRange': reviewerSkinTypeAndAgeRange[j+1],
                        'reviewTitles': reviewTitles[i],
                        'review': reviews[i]
                    }
                except IndexError:
                    self.skipRecords += 1
                    print("Number of skipped records: " + str(self.skipRecords))
                    continue
                else:
                    j = j + 4
