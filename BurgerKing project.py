# Importation of Libraries used in this project
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract Outlet Title
def get_title(soup):

    try:
        # Outer Tag Object
        store_name = soup.find('hi', attrs={'class':'card-header heading'})
        
        # Inner NavigatableString Object
        title_value = store_name.text

        # Title as a string value
        title_string = title_value.strip() 

    except AttributeError:
        title_string = ""

    return title_string 

# Function to extract Outlet Distance
def get_distance(soup):

    try:
        # Outer Tag Object
        distance = soup.find('li', attrs={'class': 'outlet-distance'})
        
        # Inner NavigatableString Object
        dis_value = distance.text

        # Title as a string value
        dis_string = dis_value.strip() 

    except AttributeError:
        dis_string = ""

    return dis_string 

# Function to extract Outlet Address
def get_address(soup):

    try:
        # Outer Tag Object
        address = soup.find('div', attrs={'class': 'info-text'})
        
        # Inner NavigatableString Object
        add_value = address.text

        # Title as a string value
        add_string = add_value.strip() 

    except AttributeError:
        add_string = ""

    return add_string

# Function to extract Outlet Pincode
def get_pincode(soup):

    try:
        # Outer Tag Object
        pin_code = soup.find('span', attrs={'class':'merge-in-next'})
        
        # Inner NavigatableString Object
        pc_value = pin_code.text

        # Title as a string value
        pc_string = pc_value.strip() 

    except AttributeError:
        pc_string = ""

    return pc_string

# Function to extract Outlet Contact-Number
def get_phonenumber(soup):

    try:
        # Outer Tag Object
        phone = soup.find('div', attrs={'class':'info-text'})
        
        # Inner NavigatableString Object
        pn_value = phone.text 

        # Title as a string value
        pn_string = pn_value.strip() 

    except AttributeError:
        pn_string = ""

    return pn_string

# Function to extract Outlet Opening Timings
def get_timimgs(soup):

    try:
        # Outer Tag Object
        timings = soup.find('li', attrs={'class':'store-clock clock-top-mng'})
        
        # Inner NavigatableString Object
        time_value = timings.text

        # Title as a string value
        time_string = time_value.strip() 

    except AttributeError:
        time_string = ""

    return time_string

# Function to extract Outlet Website-Link
def get_websitelink(soup):

    try:
        # Outer Tag Object
        website_link = soup.find('a', attrs={'class': 'btn btn-website'})
        
        # Inner NavigatableString Object
        wl_value = website_link.get('href')

        # Title as a string value
        wl_string = wl_value.strip() 

    except AttributeError:
        wl_string = ""

    return wl_string

# Function to extract Outlet Latitude(Coordinates)
def get_latitudes(soup):

    try:
        # Outer Tag Object
        latitude = soup.find('input', attrs={'class':'outlet-latitude'})
        
        # Inner NavigatableString Object
        lati_value = latitude.get('value')

        # Title as a string value
        lati_string = lati_value.strip() 

    except AttributeError:
        lati_string = ""

    return lati_string

# Function to extract Outlet Longitude(Coordinates)
def get_longitudes(soup):

    try:
        # Outer Tag Object
        longitude = soup.find('input', attrs={'class':'outlet-longitude'})
        
        # Inner NavigatableString Object
        longi_value = longitude.get('value')

        # Title as a string value
        longi_string = longi_value.strip() 

    except AttributeError:
        longi_string = ""

    return longi_string 


###############################---------CODE---------####################################

 # The webpage URL
URL = "http://stores.burgerking.in/?search=Delhi%2C+India"

# add your user agent 
HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5' })

# HTTP Request
webpage = requests.get(URL, headers=HEADERS)

# Soup Object containing all data
soup = BeautifulSoup(webpage.content, "html.parser")

# Fetch links as List of Tag Objects
links = soup.find_all('a', attrs={'onclick': "clickEventGa('store_locator', 'website_url', '178143')"})

# Store the links
links_list = []

# Loop for extracting links from Tag Objects
for link in links:
   links_list.append(link.get('href')) 

# Variable 'd' containing all info in the form of a dictionary
d = {'store-name':[], 'distance':[], 'address':[], 'pin-code':[],'phone-number':[],'timings':[],'website-link':[],'latitudes':[],'longitudes':[]}

# Loop for extracting product details from each link
for link in links_list:
  new_webpage = requests.get("https://www.burgerking.in/" + link, headers=HEADERS)
  new_soup = BeautifulSoup(new_webpage.content, "html.parser")


# Function calls to display all necessary product information
d['store-name'].append(get_title(new_soup))
d['distance'].append(get_distance(new_soup))
d['address'].append(get_address(new_soup))
d['pin-code'].append(get_pincode(new_soup))
d['phone-number'].append(get_phonenumber(new_soup))
d['timings'].append(get_timimgs(new_soup))
d['website-link'].append(get_websitelink(new_soup))
d['latitudes'].append(get_latitudes(new_soup))
d['longitudes'].append(get_longitudes(new_soup))


# Creating a csv file to store the scraped data
bk_df = pd.DataFrame.from_dict(d)
bk_df['store-name'].replace('', np.nan, inplace=True)
bk_df = bk_df.dropna(subset=['store-name'])
bk_df.to_csv("burgerking_data.csv", header=True, index=False)


