request = Request.from_curl("curl 'https://staticw2.yotpo.com/batch/app_key/kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG/domain_key/6866178441285/widget/main_widget' -H 'authority: staticw2.yotpo.com' -H 'accept: application/json' -H 'accept-language: en-US,en;q=0.8' -H 'content-type: application/x-www-form-urlencoded' -H 'origin: https://sokoglam.com' -H 'referer: https://sokoglam.com/' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: cross-site' -H 'sec-gpc: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' --data-raw 'methods=%5B%7B%22method%22%3A%22main_widget%22%2C%22params%22%3A%7B%22pid%22%3A%226866178441285%22%2C%22order_metadata_fields%22%3A%7B%7D%2C%22widget_product_id%22%3A%226866178441285%22%7D%7D%5D&app_key=kILjLgKH3AFJKWu0W8HoD8nuvs72obqsSPmWjHiG&is_mobile=false&widget_version=2023-02-08_14-34-00' --compressed")

Product Name = response.css("div.review-stars div").xpath("@data-name").extract()[0]
Product ID = response.css("div.review-stars div").xpath("@data-product-id").extract()[0]
Brand = response.css("h3.pdp__product-vendor a::text").extract()[0]
Price = response.css("span.pdp__product-price span::text").extract()[0]


response.xpath("//div[@class='content-review']/text()")