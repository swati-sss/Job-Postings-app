#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
from datetime import datetime


# In[4]:


def scrape_jobs(keywords,location):
    x = keywords.split(" ")
    x = '-'.join(x)
    y = location
    URL = "https://www.google.com/search?sxsrf=ALeKk01Xnr7_HCuYNoLg2iBiPeBW3i90AQ:1611071123974&ei=k_4GYLeHO6aF4t4P8Ki0CA&q="+x+"+in+"+y+"&oq=google+jobs&gs_lcp=CgZwc3ktYWIQAzIICAAQyQMQkQIyCggAELEDEBQQhwIyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADoECCMQJzoHCAAQsQMQQzoKCAAQsQMQgwEQQzoECAAQQzoICAAQsQMQgwE6DQgAELEDEIMBEMkDEEM6BwgAEMkDEEM6CAgAELEDEJECOgUIABDJA1CdKFjrPmCiQGgBcAF4AIABxAGIAbkMkgEEMC4xMZgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&uact=5&ibp=htl;jobs&sa=X&ved=2ahUKEwit69jVq6juAhWZ6XMBHfRDBW4QutcGKAB6BAgHEAQ&sxsrf=ALeKk036ncuofuaFDTM3LUT-PcFAHGRULg:1611071135044#fpstate=tldetail&htivrt=jobs&htidocid=hPuycPWz1n5capCdAAAAAA%3D%3D"
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe")
    page = driver.get(URL)
    scr = soup(driver.page_source, 'lxml')
    profile=[]
    company=[]
    location = []
    for i in scr.findAll('li', {'class': 'iFjolb hide-focus-ring gws-plugins-horizon-jobs__li-ed'}):
        prof = i.find('div', {'class':'BjJfJf PUpOsf'}).text.strip()
        profile.append(prof)
        name = i.find('div', {'class':'vNEEBe'}).text.strip()
        company.append(name)
        locs = i.find('div', {'class':'Qk80Jf'}).text.strip()
        location.append(locs)
    temp=[]
    sites=[]
    for locs in scr.findAll('div', {'class':'Qk80Jf'}):
        temp.append(locs.text.strip())
    for i in range(len(temp)):
        if i%2!=0:
            sites.append(temp[i])
    profile1 = []
    company1 = []
    location1 = []
    unique_file = pd.ExcelFile('D:\iSmile Technologies\Marketing analytics\Job Postings\Total_Week1_Mar.xlsx')
    un_df = pd.read_excel(unique_file,keywords,header=1)
    unique_profile = list(un_df["Profile"])
    unique_company= list(un_df["Company"])
    unique_location = list(un_df["Location"])
    for p,c,l in zip(profile, company, location):
        if p in unique_profile and c in unique_company and l in unique_location:
            continue
        else:
            unique_profile.append(p)
            unique_company.append(c)
            unique_location.append(l)
            profile1.append(p)
            company1.append(c)
            location1.append(l)
    df = pd.DataFrame(list(zip(profile1,company1, location1)), columns = ['Profile', 'Company', 'Location'])
    date = datetime.now()
    csv_name = date.strftime("%d-%m-%y")  +'-'+x+"-google-jobs-"+str(y)
    df.to_csv(str(csv_name + '.csv'), index = False)
    driver.close()
