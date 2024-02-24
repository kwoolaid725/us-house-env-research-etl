# Exploring Residential Environmental Data in the United States with a Focus on Floor Types


## Project Overview

The vacuum cleaner industry is heavily influenced by the residential environment, particularly the types of flooring found in homes. This research aimed to investigate trends in floor types in US households to support new product planning and development.

I implemented and executed ETL processes to significantly increase data collection efficiency, reducing costs by replacing automation tools with human labor, including at the managerial level. The data were extracted from Zillow, the most visited real estate website in the United States.

<img width="680" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/07679d7f-d905-4cbe-b3ec-b6dcacdcadf6">

<img width="335" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/b65de0a7-902b-433c-9a61-543752f16e2b">
<img width="340" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/8d309a94-452f-44a6-bece-79eb2aacbf9e">



![image](https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/1cd282c7-fa79-46f3-876b-da260521d9ad)
![image](https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/9a1d74e5-4cb0-4b5e-925d-ae1f104c2bbe)





## Technologies

- Beautiful Soup
- Pandas
- NumPy
- Jupyter Notebook
- Openpyxl
- Plotly
- AWS S3

----------------------------------------

## Data Extraction

- Built a scraper to gather general information about properties listed on Zillow after configuring the filters.

``` Python

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

---------------------------------------------------------

## Parameter Filters for Data to be Collected:
- 750 sq. ft. < Sq. Footage < 7,500 sq. ft.
- Built Year >= 1900
- 1+ bedroom
- The price range is set with a minimum between $100,000 and $300,000, depending on the approximate median home value of the searched metropolitan city. 

![image](https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/91e041c5-cbcb-4345-aca9-dff7b72aaefc)

----------------------------------------------------------

## Data Preprocessing:

1. Expand the initial raw data to create a number of rows based on the number of bedrooms the property has.

`data_preproccesing.ipynb`
``` Python 

# create rows according to the value in column beds
df['Beds'].value_counts()

columns = ['Built Year', 'Room', 'Floor_Type']

#insert new columns in columns to the df
for i in columns:
    df[i] = ''


# randomize the order of the rows
df = df.sample(frac=1).reset_index(drop=True)


beds_to_room = {1: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Basement'],
                2: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Basement'],
                3: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Basement'],
                4: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Basement'],
                5: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Bed_Others', 'Basement'],
                6: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Bed_Others', 'Basement'],
                7: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Bed_Others', 'Basement'],
                8: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Bed_Others', 'Basement'],
                9: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Bed_Others', 'Basement'],
                10: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Bed_Others', 'Basement'],
                11: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Bed_Others', 'Basement'],
                12: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Bed_Others', 'Basement'],
                13: ['Living', 'Dining', 'Family', 'Kitchen', 'Bed', 'Bed2', 'Bed3', 'Bed4', 'Bed_Others', 'Basement']}

df['Room'] = df.groupby('ZPID')['Beds'].apply(lambda x: x.map(beds_to_room))

```

2. Divide the dataframe into groups corresponding to the number of people who will be manually sorting the floor types.  
   In this case, four people will be assigned to this task.


   ``` Python
    # divide the df into 4 parts
    df1 = df.iloc[:int(df.shape[0]/5), :]
    print(len(df1))
    df1= df1.explode('Room')

    df2 = df.iloc[int(df.shape[0]/5):int(df.shape[0]/5*2), :]
    print(len(df2))
    df2= df2.explode('Room')
   
    df3 = df.iloc[int(df.shape[0]/5*2):int(df.shape[0]/5*3.5), :]
    print(len(df3))
    df3= df3.explode('Room')

    df4 = df.iloc[int(df.shape[0]/5*3.5):, :]
    print(len(df4))
    df4= df4.explode('Room')
   ```

3. Save the randomly split dataframe into Excel worksheets to distribute to the workers, with thick borders added around each property for the workers' convenience.

``` Python

from openpyxl.styles import Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook

wb1 = Workbook()
ws1 = wb1.active

for r in dataframe_to_rows(df1, index=False, header=True):
    ws1.append(r)

# initialize the last_seen variable with None
last_seen = None

# set the border properties for the last cell with a unique ZPID
for row in ws1.iter_rows(min_row=2, max_row=ws1.max_row, min_col=1, max_col=ws1.max_column):
    current_zpid = row[0].value
    if current_zpid != last_seen:
        # if the current ZPID is different from the last seen ZPID, set the border for the last cell with the last seen ZPID
        for cell in row[:]:
            cell.border = Border(top=Side(style='thick'))
    last_seen = current_zpid


wb1.save('xxxx.xlsx')

```
output: 

![image](https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/356a0e45-458d-4660-8030-5a7eb28476d3)

### The reason 'Built Year' and 'Floor Type' cells are blank is:

- Collecting built-year data automatically would have required an additional step, such as using a separate scraper. Therefore, I've figured it's not time-efficient to run an extra scraper solely for obtaining built-year data.
- The floor type information can only be obtained manually by inspecting the pictures.

Therefore, the two columns were left blank to be filled in by manual workers by accessing the hyperlinks provided.

-----------------------------------------------------------
## Data Analysis 

### 1. Researched states represented in color fills by each region
<img width="600" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/6f7102fb-e039-4aff-bb95-21de220f1e28">

### 2. What the distribution of randomly collected data looks like
![image](https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/df2d818f-33d5-476e-8666-36caf5d8d470)


### 3. Choropleth Map: Median House Price and Avg. House Built-Years
<img width="324" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/89788b12-46f0-4eb0-a84d-0c973111469a">
<img width="325" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/fd88913f-a195-41fb-a7f9-92d2a0e0ec47">

### 4. Floor Type Distribution Results

##### - Overall Floor Types by Each Room Type 

<img width="600" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/2f48c9f0-2890-4c34-a961-6d6b07228e56">

- More than half of all bedrooms across the nation have carpeted floors (56%)
- About half of all living rooms across the nation have rugs on top of the bare floors.

##### - Bedrooms By Regions & States

<img width="344" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/5981f1a0-c7bd-4e55-9704-554c8f0687b3">
<img width="373" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/4c30ffdd-9edd-420b-b51d-101a351a32b3">
<img width="352" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/ac7ec38c-32eb-4e30-8cf0-8e9c15c59fd4">

- Midwest region has the highest carpeted bedrooms ratio
- Mountain states in West region also have significantly high carpeted bedrooms ratio

##### - Bedrooms By Regions & Division: Midwest 
<img width="705" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/ab2a89ec-e157-48d2-b237-9738a5c7f644">

##### - Bedrooms By Regions & Division: Northeast
<img width="699" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/a4a27a0d-605d-4f84-98fb-6de13aa3e482">

##### - Bedrooms By Regions & Division: South
<img width="713" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/2fe1565c-a56b-4f03-bfdd-266fc4c575d5">

##### - Bedrooms By Regions & Division: West
<img width="711" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/8b39ba1e-ca74-4fd0-b44b-146058873a35">

##### - Living Rooms By Regions & States
<img width="717" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/07587a1e-a2f9-4b39-8daa-61c2d622de4a">

- Midwest region has the highest living rooms ratios

##### - Living Rooms By Regions & Divisions: Midwest
<img width="705" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/a1ab35e4-2d2a-4c25-b290-44b6b39ce4f2">

##### - Living Rooms By Regions & Divisions: Northeast
<img width="700" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/9f71e01e-e8f6-405c-8189-8d8649c1d9b0">

##### - Living Rooms By Regions & Divisions: South
<img width="713" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/8e4c2fc7-e9bc-4ee8-a02f-1f36c432be63">

##### - Living Rooms By Regions & Divisions: West
<img width="714" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/c77a2e1e-e842-4fc5-8b46-425f6556b394">

##### - Basements By Regions and States
<img width="718" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/7ffc700c-eef9-4c5d-8348-0c316276b583">

- West region has the highest carpeted basement ratio

##### - Basements By Regions & Divisions: Midwest
<img width="705" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/c12cab21-2a90-42c8-8bee-96f7894e1d97">

##### - Basements By Regions & Divisions: Northeast
<img width="700" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/8b09a086-3ab3-4d01-8ea5-5e9269afd714">

##### - Basements By Regions & Divisions: South
<img width="713" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/16fe7bbd-e8c6-493e-a012-64a70ce624ce">

##### - Basements By Regions & Divisions: West
<img width="710" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/65626ff8-059c-4073-8a07-77f27726696e">

##### - Other Rooms By Regions
<img width="704" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/0d78400c-ab92-4b62-94e4-ba37f15d2ef0">

##### - Home Type vs. Carpeted Bedrooms %
<img width="598" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/b38cdced-3d83-47e4-89a9-7a6eb5233f41">

##### - Built Year vs. Carpeted Bedrooms %
<img width="583" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/c1dd81df-3799-4e1d-b78d-9a150e7dfbb3">


##### - Built Year vs. Carpeted Bedrooms % : MIDWEST top 3 States

`Illinois`
<img width="426" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/e86ba39d-1c0a-41b5-9c13-793baa7c7d22">

`Ohio`
<img width="438" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/8ec68954-0dde-4fa0-9e26-6e3073bce9c3">

`Missouri` 
<img width="438" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/4fa31bb6-30de-4c83-ba91-688a30c4467e">

##### - Built Year vs. Carpeted Bedrooms % : NORTHEAST top 3 States

`New York`
<img width="401" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/3b80d387-c55f-4c26-95d5-f2aabb5ae93a">

`New Jersey`
<img width="428" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/224ea299-e801-4201-af6a-e0a55456e06c">

`Massachusetts`
<img width="415" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/d011d1a0-2172-40a4-8934-05e57c17355f">

##### - Built Year vs. Carpeted Bedrooms % : WEST top 3 States

`California`
<img width="411" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/8f71c86e-b53a-4de9-98ba-be543c14b96a">

`Arizona`
<img width="411" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/7b7f3926-c419-4111-ad29-11f258b8dbe1">

`Washington`
<img width="417" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/6340a475-1b61-4b9a-8bb6-ca0b0ad8b49d">

##### - Built Year vs. Carpeted Bedrooms % : SOUTH top 3 States

`Texas`
<img width="416" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/4942f507-8657-4502-a43e-eb7facffa4ad">

`Florida`
<img width="414" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/3b8a7a44-4b21-4c08-b591-336408ee1a1e">

`Tennessee`
<img width="416" alt="image" src="https://github.com/kwoolaid725/us-house-env-research-etl/assets/107806433/e845fad5-93b9-4eb4-a634-5c8b4dcb89d5">

-----------------------------------------------------------
## Conclusions derived from analyzing the data

Initially, I hypothesized that cold regions like the Northeast would generally have a higher ratio of carpeted floors, but the data suggested otherwise.

Possible reasons for it having more bare floor types, such as hardwood and tiles

`i) The Northeast region has the oldest houses compared to other regions due to its long history of habitation.`

`ii) The Northeast region has a higher proportion of wealthy households that can afford renovations, as hardwood floors are more expensive to install than carpeted floors.`

The above assumptions can also be supported by the fact that rapidly growing states like Texas and Arizona have a higher percentage of newer homes, resulting in a higher ratio of carpeted floors despite the hot climate.

----------------------------------------------------------------
## Key takeaways based on the conclusion 🗝️

- The regions with affluence and longer history seem to have a greater impact on floor types than the climate, thus targeted product development and marketing strategies are necessary.
- The ratio of houses with carpeted floors will not be decreasing any time soon, as newer homes are generally built with carpets. Therefore, it remains important to develop vacuum cleaners that can effectively clean carpets.
- The insight aligns with market data showing that upright vacuums still dominate higher market shares, as they are generally more capable and reliable in cleaning carpeted floors.

