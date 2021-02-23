#!/usr/bin/env python
# coding: utf-8

# In[8]:


from bs4 import BeautifulSoup 
import requests
import re
import pandas as pd


# In[2]:


def start(link):
    
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    source = requests.get(link, headers = headers).text
    soup = BeautifulSoup(source, 'lxml')
    return soup

def getclasses(soup_temp):
    classes = soup_temp.findAll("div", {"class": "_8ssblpx"})
    res = []
    for i in classes:
        res.append(i)
    return res


# In[3]:


def name(record):
    item_name = record.find("meta")["content"]
    return item_name

def description(record):
    item_description = record.find("div", {"class": "_167qordg"}).text
    return item_description

def price(record):
    item_price = record.find("div", {"class":"_1fwiw8gv"}).text
    return item_price

def roominfo(record):
    item_roominfo = record.find("div", {"class":"_kqh46o"}).text
    return item_roominfo

def facility(record):
    try:
        item_facilities = record.findAll("div", {"class":"_kqh46o"})[1].text.replace(" ","")
    except:
        item_facilities = []
    return item_facilities

def rating(record):
    item_rating = record.find("span", {"class":"_krjbj"}).text
    return item_rating


def review_number(record):
    try:
        item_review_number = record.findAll("span", {"class":"_krjbj"})[1].text
    except:
        item_review_number = None
    return item_review_number

def link(record):
    item_link = "http://airbnb.com" + record.find("a")["href"]  
    return item_link


# In[4]:


def getinfo(soup_temp):
    records = getclasses(soup_temp)
    names = []
    descriptions = []
    prices = []
    info = []
    facilities = []
    ratings = []
    review_numbers = []
    links = []
    for record in records:
        names.append(name(record))
        links.append(link(record))
        descriptions.append(description(record))
        info.append(roominfo(record))
        facilities.append(facility(record))
        prices.append(price(record))
        ratings.append(rating(record))
        review_numbers.append(review_number(record))
    dfcolumns = {"Names": names, "Descriptions": descriptions, "Prices": prices, "Info": info, "Facilities" : facilities, "Ratings": ratings, "Review number": review_numbers, "Links": links}
    return pd.DataFrame(dfcolumns)


# In[5]:


def nextpage(soup_temp):
    try:
        nextpage = "https://airbnb.com" + soup_temp.find("li", {"class": "_i66xk8d"}).find("a")["href"]
    except:
        nextpage = "no next page"
    return nextpage

def allpages(link):
    res = []
    while link != "no next page": 
        page = start(link)
        res = res + [page]
        link = nextpage(page)
    return res

def extractallpages(link):
    pages = allpages(link)
    df = getinfo(pages[0])
    for i in range(1, len(pages)):
        df = df.append(getinfo(pages[i]))
    return df


# In[6]:


new_york = 'https://www.airbnb.com/s/New-York--NY--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&place_id=ChIJOwg_06VPwokRYv534QaPC8g'
chicago = 'https://www.airbnb.com/s/Chicago--IL--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&query=Chicago%2C%20IL%2C%20United%20States&place_id=ChIJ7cv00DwsDogRAMDACa2m4K8'
boston = 'https://www.airbnb.com/s/Boston--MA--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&query=Boston%2C%20MA%2C%20United%20States&place_id=ChIJGzE9DS1l44kRoOhiASS_fHg'
san_francisco = 'https://www.airbnb.com/s/San-Francisco--CA--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&query=San%20Francisco%2C%20CA%2C%20United%20States&place_id=ChIJIQBpAG2ahYAR_6128GcTUEo'
los_angeles = 'https://www.airbnb.com/s/Los-Angeles--CA--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&query=Los%20Angeles%2C%20CA%2C%20United%20States&place_id=ChIJE9on3F3HwoAR9AhGJW_fL-I'


# In[9]:


nyc = extractallpages(new_york)
chc= extractallpages(chicago)
bst = extractallpages(boston)
sf = extractallpages(san_francisco)
la = extractallpages(los_angeles)


# In[10]:


nyc['City']='New York'
la['City']='Los Angeles'
chc['City']='Chicago'
bst['City']='Boston'
sf['City']='San Francisco'


# In[11]:


airbnb_raw = pd.concat([nyc, la, chc, bst, sf])


# In[12]:


airbnb_raw.head()


# In[13]:


airbnb_raw.to_csv('airbnb_raw.csv')


# In[ ]:




