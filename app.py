import flask
from flask import Flask,request, jsonify,render_template
import numpy as np
import pickle
import pandas as pd
import sys
sys.path.append('D:\\iSmile Technologies\\Marketing analytics\\Web Scraping App')
import google_job_scraping
import monster_job_scraping
import linkedin_job_scraping
import indeed_job_scraping
app=Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return(render_template('Final_Web_Scraping_UI.html'))

@app.route('/download',methods=['POST'])
def download():
    data=[i for i in request.form.values()]
    web=request.form['website']
    key=request.form['keywords']
    loc=request.form['location']
    if(web=='Google Jobs' and key!='All'):
    	google_job_scraping.scrape_jobs(key,loc)
    elif(web=='LinkedIn Jobs' and key!='All'):
    	linkedin_job_scraping.scrape_jobs(key,loc)
    elif(web=='Indeed Jobs' and key!='All'):
    	indeed_job_scraping.scrape_jobs(key,loc)
    elif(web=='Monster Jobs' and key!='All'):
    	monster_job_scraping.scrape_jobs(key,loc)
    elif(web=='All' and key!='All'):
    	google_job_scraping.scrape_jobs(key,loc)
    	linkedin_job_scraping.scrape_jobs(key,loc)
    	indeed_job_scraping.scrape_jobs(key,loc)
    	monster_job_scraping.scrape_jobs(key,loc)
    websites=['google_job_scraping','linkedin_job_scraping','indeed_job_scraping','monster_job_scraping']
    k=['AWS Cloud','Azure Cloud','Google Chrome Enterprise','Google Cloud','Google For Education','Google Workspace','G-suite']
    if(key=='All' and web=='All'):
    	for i in k:
    	    for j in websites:
    	    	j.scrape_jobs(k,loc)
    if(key=='All' and web=='Google Jobs'):
        for i in k:
            google_job_scraping.scrape_jobs(i,loc)
    if(key=='All' and web=='LinkedIn Jobs'):
    	for i in k:
    	    linkedin_job_scraping.scrape_jobs(i,loc)
    if(key=='All' and web=='Indeed Jobs'):
    	for i in k:
    	    indeed_job_scraping.scrape_jobs(i,loc)
    if(key=='All' and web=='Monster Jobs'):
    	for i in k:
    	    monster_job_scraping.scrape_jobs(i,loc)
    return(render_template('Final_Web_Scraping_UI.html',download_text='{} File downloaded for {} portal'.format(key,web)))
    
if __name__=='__main__':
    app.run(debug=True)