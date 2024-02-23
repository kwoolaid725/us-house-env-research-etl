# Exploring Residential Environmental Data in the United States with a Focus on Floor Types

## Project Overview

The vacuum cleaner industry is heavily influenced by the residential environment, particularly the types of flooring found in homes. This research aimed to investigate trends in floor types in US households to support new product planning and development.

I implemented and executed ETL processes to significantly increase data collection efficiency, reducing costs by replacing automation tools with human labor, including at the managerial level. The data were extracted from Zillow, the most visited real estate website in the United States.

<img width="817" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/f1bb1f1d-5a8a-4f8d-9494-c9381a040847">

## Technologies

- Beautiful Soup
- Pandas
- NumPy
- Jupyter Notebook
- Openpyxl
- Plotly
- AWS S3

## Data Extraction

- Built a scraper to gather general information about properties listed on Zillow after configuring the filters.

```
import os

from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time


def get_headers():
    # Creating headers.
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, sdch, br',
               'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
               'cache-control': 'max-age=0',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    return headers

def save_to_file(response):
    # saving response to `response.html`

    with open("response.html", 'w') as fp:
        fp.write(response.text)


def getdata(url):
    payload = {'api_key': 'api_key', 'url': url, 'keep_headers': 'true'}

    for i in range(5):
        r = requests.get('http://api.scraperapi.com', params=payload, headers=headers, timeout=60)
        print("status code received:", r.status_code)
        if r.status_code != 200:
            # saving response to file for debugging purpose.
            continue
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup


def get_properties(json_data):
    item_list = json_data['cat1']['searchResults']['listResults']

    for item in item_list:
        zpid = item['zpid']
        detail_url = item['detailUrl']
        state = item['addressState']
        city = item['addressCity']
        address = item['address']
        zipcode = item['addressZipcode']
        home_type = item['hdpData']['homeInfo']['homeType']
        price = item['unformattedPrice']
        sq_ft_area = item['area']
        beds = item['beds']
        baths = item['baths']
        # if item['latLong'] == {}:
        #     latitude = ''
        #     longitude = ''
        # else:
        #     latitude = item['latLong']['latitude']
        #     longitude = item['latLong']['longitude']

        res = {
            'ZPID': zpid,
            'URL': detail_url,
            'Region': region,
            'State': state,
            'City': city,
            'Zipcode': zipcode,
            'Address': address,
            'Home_Type': home_type,
            'Home_Price': price,
            'Sq_ft': sq_ft_area,
            'Beds': beds,
            'Baths': baths,
            # 'floor_type': floortype_search,
            # 'latitude': latitude,
            # 'longitude': longitude


        }
        results.append(res)

    return results



headers = get_headers()
region = 'West'



x = 1
while x <= 10:
    results = []
    url = f'https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22usersSearchTerm%22%3A%22LA%22%2C%22mapBounds%22%3A%7B%22north%22%3A35.17168652569004%2C%22east%22%3A-115.52634805977304%2C%22south%22%3A33.26178291269555%2C%22west%22%3A-120.49766153633554%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22min%22%3A300000%7D%2C%22mp%22%3A%7B%22min%22%3A1504%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22sqft%22%3A%7B%22min%22%3A750%7D%2C%22built%22%3A%7B%22min%22%3A1900%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A9%2C%22pagination%22%3A%7B%22currentPage%22%3A{x}%7D%7D'
    soup = getdata(f'{url}')
    time.sleep(1)

    print(f'Page: {x}')
    script_tag = soup.find('script', {'data-zrr-shared-data-key': 'mobileSearchPageStore', 'type': 'application/json'})

    time.sleep(1)
    raw_json_data = script_tag.contents[0]
    clean_json_data = raw_json_data.replace('<!--', '').replace('-->', '')
    json_data = json.loads(clean_json_data)

    time.sleep(1)
    get_properties(json_data)
    print(len(results))
    df = pd.DataFrame(results)
    df.to_csv(f'Region_{region}.csv',
              mode='a', index=False, header=not os.path.exists(f'Region_{region}.csv'),
              encoding='utf-8-sig')
    x += 1




```






<img width="468" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/ba639dba-00b2-43c9-8384-96da815188d9">

<img width="469" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/b9252244-8877-4bfa-90a0-56e909c47cc3">



<img width="468" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/26bbeec4-42bd-4fa9-8270-5849a67154fc">

<img width="468" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/41e619d9-4c0f-460f-8164-361affa0a4d7">

<img width="468" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/76a49eb7-fc1e-49ed-8657-f1fca65ae86a">
