import requests, json
from time import sleep
import pandas as pd


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location(ip_address: int,ip_range: str) -> dict:
    ''' 
    take an ip with corresponding ip range after cleaning
    and returns dictionary with location metadata
    '''
    #ip_address = get_ip()
    #response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    response = requests.get(f'http://ip-api.com/json/{ip_address}').json()
    location_data = {
        "ip": ip_address,
        "ip_range": ip_range,
        "city": response.get("city"),
        "region": response.get("region"),
        "region_name": response.get("regionName"),
        "country": response.get("country"),
        "country_code": response.get("countryCode"),
        "lat": response.get("lat"),
        "lon": response.get("lon")
    }
    return location_data

def dl_json(url: str) -> dict:
    ''' 
    Download a json file
    '''
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Failed to download data from {url} with status code {response.status_code}')
    

def create_ip_dict(ip_dict: dict) -> list[dict]:
    '''
    adds location metadata to an ip / ip range 
    note: sleep(1.5) -> 45 requests a min which is the limit for free api
    '''
    ip_meta = []
    for ip,ipr in ip_dict.items():
        ip_add = get_location(ip,ipr)        
        ip_meta.append(ip_add)
        #print(ip)
        sleep(1.6)
    return ip_meta

url = 'http://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20241021.json'
json_data = dl_json(url)

json_data_pbi = json_data['values'][75]['properties']['addressPrefixes']

pbi_cleaned = {prefix.split('/')[0]: prefix for prefix in json_data_pbi}

pbi_meta = create_ip_dict(pbi_cleaned)

pbi_df = pd.DataFrame(pbi_meta)
pbi_df

pbi_EUN = pbi_df.loc[pbi_df['country_code'] == 'IE']
pbi_EUN
