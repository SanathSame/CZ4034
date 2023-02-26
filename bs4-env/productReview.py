import requests
import csv
from bs4 import BeautifulSoup
import time

# Open the input CSV file and read the URLs
with open('productlist.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    productIDs = [row['product_ID'] for row in reader]
    names = [row['product_name'] for row in reader]

# Create an output CSV file and write the headers

# URL + Parameter + pageNum
URL = "https://staticw2.yotpo.com/batch/app_key/kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG/domain_key/9595478921/widget/reviews"

headers = {
    'authority': 'staticw2.yotpo.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.5',
    'origin': 'https://sokoglam.com',
    'referer': 'https://sokoglam.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
skipped = 0
total_pages = 0
with open('productReviews_soup.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # csv_writer.writerow(['Product_ID', 'Product_Name',
    #                    'Reviewer', 'Review_Title', 'Review'])

    # Loop through the URLs and scrape the reviews
    crawled = 0
    start_time = time.time()
    for productID in productIDs:
        page_number = 1
        if crawled < 226:
            crawled += 1
            continue
        while True:
            if crawled == 226 and page_number < 4:
                page_number+=1
                continue
            print("Page No.: " + str(page_number))
            print("Products Crawled: " + str(crawled))
            print("Total Pages Crawled: " + str(total_pages))

            # Make a request to the URL
            data = {
                'methods': '[{"method":"reviews","params":{"pid":"'+str(productID)+'","order_metadata_fields":{},"widget_product_id":"'+str(productID)+'","data_source":"default","page":'+str(page_number)+',"host-widget":"main_widget","is_mobile":false,"pictures_per_review":10}}]',
                'app_key': 'kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG',
                'is_mobile': 'false',
                'widget_version': '2023-02-13_11-23-53',
            }

            response = requests.post(URL, headers=headers, data=data)
            # Check if the page exists
            if response.status_code != 200:
                print("Page don't exist!")
                print("Product Name: " + str(productName))
                break

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.json()[0]['result'], 'html.parser')

            # Find all the reviews
            reviews = soup.find_all('div', {'class': 'content-review'})

            # Skip to next product if 0 reviews
            if len(reviews) == 0:
                break

            try:
                productName = soup.find(
                    'div', {'class': 'y-label product-link'}).string.split("On ")[1]
                print("Product Name: " + str(productName))
            except AttributeError:
                skipped += 1
                print("0 Reviews")
                break

            # List of reviewers
            try:
                reviewers = soup.find_all(
                    'span', {'class': 'y-label yotpo-user-name yotpo-font-bold pull-left'})
            except IndexError:
                skipped += 1
                print("0 Reviews")
                break

            # list of skinType + ageRange (i = i+2 two record per person)
            # reviewerSkinTypeAndAgeRange = soup.find_all(
            #   'span', {'class': 'yotpo-user-field-answer text-s'})

            # list of reviews title
            reviewTitles = soup.find_all(
                'div', {'class': 'content-title yotpo-font-bold'})

            # Exporting data to csv
            for i in range(len(reviews)):
                if i == 5:
                    break
                review = reviews[i].string
                if type(review) == 'NoneType':
                    continue

                try:
                    reviewer = reviewers[i].string
                except IndexError:
                    skipped += 1
                    print("Reviewer empty")
                    break

                reviewTitle = reviewTitles[i].string
                # Write the data to the output CSV file
                csv_writer.writerow(
                    [productID, productName, reviewer, reviewTitle, review])

            # Increase the page number for the next request
            page_number += 1
            total_pages+=1
        crawled += 1

    end_time = time.time()
    total_minutes = (end_time - start_time)/60
    total_hours = total_minutes/60
    if (total_hours < 1):
        print("Time taken: " + str(total_minutes) + " minutes")
    else:
        print("Time taken: " + str(total_hours) + " hours")
