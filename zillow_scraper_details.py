import csv
import pandas as pd
import numpy as np
import os

from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time
from datetime import datetime
from tqdm import tqdm

pd.set_option('mode.chained_assignment', None)

headers_ = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

def zpid_to_soup(url):
    time.sleep(0.5)
    url = url
    payload = {'api_key': 'c52bb0af37f8185b7950a05e932725fb', 'url': url, 'keep_headers': 'true'}
    time.sleep(1)
    for i in range(3):
        r = requests.get('http://api.scraperapi.com', params=payload, headers=headers_, timeout=60)
        print("status code received:", r.status_code)
        time.sleep(1)
        if r.status_code != 200:
            # saving response to file for debugging purpose.
            return r.status_code
            continue
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            return soup

def get_data_from_soup(soup):
    if soup == 500:
        return None
    else:
        json_data = [json.loads(x.string, strict=False ) for x in soup.find_all("script", id="__NEXT_DATA__", type="application/json")]
        time.sleep(1)
        if json_data == []:
            return None
        else:
            time.sleep(0.5)
            json_data_loaded = json.loads(json_data[0]["props"]["pageProps"]["gdpClientCache"])
            if json_data_loaded == []:
                return None
            else:
                data = json_data_loaded[f'NotForSaleShopperPlatformFullRenderQuery{{"zpid":{zpid}}}']['property']
                return data


# Load the input CSV file
df = pd.read_csv('zillows_NY_input.csv')



error_rows = []
# Define header for CSV file
header = ['zpid', 'detail_url', 'state', 'city', 'zipcode', 'address', 'home_type', 'price', 'sq_ft_area', 'beds', 'baths', 'levels', 'yearBuilt', 'bathroomsFull', 'bathroomsHalf', 'bathroomsThreeQuarter', 'basement', 'flooring', 'rooms', 'heating', 'cooling', 'description', 'zestimate', 'longitude', 'latitude']
header2 = ['zpid', 'detail_url', 'state', 'city', 'zipcode', 'address', 'home_type', 'price', 'sq_ft_area', 'beds', 'baths']
# Open CSV file for writing
with open('zillows_NY_output.csv', mode='a', newline='', encoding='utf-8-sig') as file, open('error.csv', mode='a', newline='', encoding='utf-8-sig') as error_file:
    writer = csv.writer(file)
    error_writer = csv.writer(error_file)
    if file.tell() == 0:
        writer.writerow(header)  # Write header to CSV file
    elif error_file.tell() == 0:
        error_writer.writerow(header2)
    else:
        pass
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        zpid = row['zpid']
        url = row['detail_url']
        time.sleep(1)
        soup = zpid_to_soup(url)
        time.sleep(1)
        data = get_data_from_soup(soup)
        if data == None:
            print("data not found for zpid:", zpid, "thus skipping this zpid")
            error_writer.writerow([zpid, url, row['state'], row['city'], row['zipcode'], row['address'], row['home_type'], row['price'], row['sq_ft_area'], row['beds'], row['baths']])
            continue
        else:
            print(zpid)
            pass
        output_row = [zpid, url, row['state'], row['city'], row['zipcode'], row['address'], row['home_type'],
                      row['price'], row['sq_ft_area'], row['beds'], row['baths'], data['resoFacts']['levels'], data['yearBuilt'],
                      data['resoFacts']['bathroomsFull'],data['resoFacts']['bathroomsHalf'], data['resoFacts']['bathroomsThreeQuarter'],
                      data['resoFacts']['basement'], data['resoFacts']['flooring'], np.array(data['resoFacts']['rooms']).ravel(),
                      data['resoFacts']['heating'], data['resoFacts']['cooling'], data['description'], data['zestimate'], data['longitude'], data['latitude']]
        writer.writerow(output_row)  # Write output row to CSV file
        time.sleep(1)

