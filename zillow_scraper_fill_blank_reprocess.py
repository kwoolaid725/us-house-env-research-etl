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

# headers_ =

def zpid_to_soup(url):
    url = url
    payload = {'api_key': '0a53d12b168b28c41638451a545f7495', 'url': url, 'keep_headers': 'true'}
    # time.sleep(1)
    r = requests.get('http://api.scraperapi.com', params=payload,
                headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'})
    print("status code received:", r.status_code)
    # time.sleep(1)

    if r.status_code != 200:
        # saving response to file for debugging purpose.
        return None
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup

def get_data_from_soup(soup):
    json_data = [json.loads(x.string, strict=False) for x in
                 soup.find_all("script", id="hdpApolloPreloadedData", type="application/json")]
    print(json_data)
    if json_data == []:

        json_data = [json.loads(x.string, strict=False) for x in
                     soup.find_all("script", id="__NEXT_DATA__", type="application/json")]
        if json_data == []:
            return None
        else:
            data1 = json.loads(json_data[0]["props"]["pageProps"]["gdpClientCache"])
            data = data1[list(data1.keys())[0]]
            # time.sleep(0.5)
            # json_data_loaded = json.loads(json_data[0]["props"]["pageProps"]["gdpClientCache"])
            return data
    else:
        # time.sleep(0.5)
        data1 = json.loads(json_data[0]["apiCache"])
        data = data1[list(data1.keys())[0]]

        return data


# Load the input CSV file


error_rows = []
# Define header for CSV file
header = ['ZPID', 'URL', 'Region', 'State', 'City', 'Zipcode', 'Address', 'Home_Price', 'Home_Type', 'Sq_ft', 'Built_Year', 'Beds', 'Baths', 'FloorLevels', 'Room','FloorType','Rug']
header2 = ['zpid']

df = pd.read_csv('NorthEast_1.csv')


# Open CSV file for writing
with open('testststes.csv', mode='a', newline='', encoding='utf-8-sig') as file, open('error.csv', mode='a', newline='', encoding='utf-8-sig') as error_file:
    writer = csv.writer(file)
    error_writer = csv.writer(error_file)
    if file.tell() == 0:
        writer.writerow(header)  # Write header to CSV file
    elif error_file.tell() == 0:
        error_writer.writerow(header2)
    else:
        pass
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        zpid = row['ZPID']
        url = row['URL']
        region = row['Region']
        state = row['State']
        city = row['City']
        zipcode = row['Zipcode']
        address = row['Address']
        home_type = row['Home_Type']
        home_price = row['Home_Price']
        sq_ft = row['Sq_ft']
        beds_no = row['Beds']
        baths_no = row['Baths']

        time.sleep(1)
        soup = zpid_to_soup(url)
        time.sleep(1)
        if soup == None:
            print("soup not found for zpid:", zpid, "thus skipping this zpid")
            error_writer.writerow([zpid])
            continue
        else:
            pass
        data = get_data_from_soup(soup)
        if data == None:
            print("data not found for zpid:", zpid, "thus skipping this zpid")
            error_writer.writerow([zpid])
            continue
        else:
            print(zpid)
            pass
        output_row = [zpid, url, region, state, city, zipcode, address, home_price, home_type, sq_ft,
                      data['property']['yearBuilt'],  beds_no, baths_no ]


        writer.writerow(output_row)  # Write output row to CSV file
        time.sleep(1)



