#!/usr/bin/env python
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
from datetime import datetime
from flask import render_template

# In[12]:


def scrape_jobs(keywords,location):
    #render_template('Final_Web_Scraping_UI.html',processing_text='Monster job scraping is in progess please wait')
    x = keywords.split(" ")
    x = '-'.join(x)
    y = location
    URL = "https://www.monster.com/jobs/search/?q="+x+"&where="+y+"&stpage=1&page=10"
    page = requests.get(URL)
    scr = soup(page.content, 'lxml')
    profile=[]
    for header in scr.findAll('h2', {'class':'title'}):
        profile.append(header.text.strip())
    company=[]
    for name in scr.findAll('div', {'class':'company'}):
        company.append(name.text.strip())

    location=[]
    for locs in scr.findAll('div', {'class':'location'}):
        location.append(locs.text.strip())
    location = location[1:]

    posted_on=[]
    for post in scr.findAll('div', {'class':'meta flex-col'}):
        posted_on.append(post.text.strip())
    for i in range(len(posted_on)):
        if len(posted_on[i])<30:
            a = posted_on[i].split(" ", 2 )
            b = a[0]+" " +a[1] + " ago"
            posted_on[i] = b
        else:
            posted_on[i] = "Posted today"
    profile1 = []
    company1 = []
    location1 = []
    unique_file = pd.ExcelFile('D:\iSmile Technologies\Marketing analytics\Job Postings\Total_Week1_Mar.xlsx')
    un_df = pd.read_excel(unique_file,keywords,header=1)
    print(un_df.head())
    unique_profile = list(un_df["Profile"])
    unique_company= list(un_df["Company"])
    unique_location = list(un_df["Location"])
    count=0
    for p,c,l in zip(profile, company, location):
        if p in unique_profile and c in unique_company and l in unique_location:
            count=count+1
            continue
        else:
            unique_profile.append(p)
            unique_company.append(c)
            unique_location.append(l)
            profile1.append(p)
            company1.append(c)
            location1.append(l)
    print('{} duplicate records found'.format(count))
    df = pd.DataFrame(list(zip(profile1,company1, location1)), columns = ['Profile', 'Company', 'Location'])
    date = datetime.now()
    
    csv_name = date.strftime("%d-%m-%y") +'-'+x+"-monster-jobs-"+str(y)
    df.to_csv(str(csv_name + '.csv'), index = False)