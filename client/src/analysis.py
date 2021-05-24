# -*- coding: utf-8 -*-
"""
Created on Sun May 23 15:12:17 2021

@author: quint


import couchdb
couch = couchdb.Server()


couch = couchdb.Server('https://dbuser::dibhd59lka@localhost:5984/')


import requests

url = "http://dbuser:dibhd59lka@localhost:5984/tweets/_design/test_view/_view/sleepview"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


"""

import json

import pandas as pd    
from pandas.io.json import json_normalize
import string
import plotly.graph_objects as go
import emoji
import numpy as np


with open('tweets.json', encoding = 'utf-8') as f:
  data = json.load(f)

total_rows = data['total_rows']

tweet_list = data['rows']


"""Pre-Processing"""

import time
# plus 11 because we are +11 from GMT

def timetohour(gmt_time):
    
    hour = (gmt_time[3]+11) % 24 
    return hour


hour24_list = []
date_year = []
date_month = []
text_list = []
location = []

# Extract data from tweets into lists

for tweet in tweet_list:
    gmt_time = time.gmtime(tweet['key'][0])
    hour24_list.append(timetohour(gmt_time))
    date_year.append((gmt_time[0]) )
    date_month.append((gmt_time[1]))
    text_list.append(tweet['value'][0])
    location.append(tweet['value'][1]['full_name'])
 
    
# Clean location data any points within a give state are assigned to the captial   
    # store points in australia by index
clean_loc = [] 
index = []
count = 0
for loc in  location:
    clean = loc.translate(str.maketrans('', '', string.punctuation))
    tokens = set(clean.lower().split())
    
    if 'adelaide' in tokens:
        clean_loc.append('adelaide')
        index.append(count)
    if 'western' in tokens and 'australia' in tokens:
        clean_loc.append('perth')
        index.append(count)
    if 'queensland' in tokens:
        clean_loc.append('brisbane')
        index.append(count)
    if 'south'  in tokens and 'new' in tokens and 'wales' in tokens:
        clean_loc.append('sydney')
        index.append(count)
    if 'tasmania' in tokens:
        clean_loc.append('hobart')
        index.append(count)
    if 'northern' in tokens and 'territory' in tokens:
        clean_loc.append('darwin')
        index.append(count)
    if 'victoria' in tokens:
        clean_loc.append('melbourne')
        index.append(count)
    if 'canberra' in tokens:
        clean_loc.append('canberra')
        index.append(count)
    
    count += 1
    





    
# Only store tweets location in australia based on index    
hour24_list = [hour24_list[i] for i in index]    
date_year = [date_year[i] for i in index]    
date_month = [date_month[i] for i in index]    
text_list = [text_list[i] for i in index]    
location = [location[i] for i in index]    
 
    

d = {'24_hour' : hour24_list, 'date_year' : date_year, 'date_month' :date_month ,
     'text' : text_list, 'location' : location, 'clean_loc' : clean_loc}

df = pd.DataFrame(d)
# seperate dataframe into before and during covid

idx = np.where((df['date_year']>= 2020) & (df['date_month'] >= 3) )

during19_df = df.loc[idx]
before19_df = df.drop(idx[0], axis=0)



"""SLEEP"""


awake_before_late = 0
awake_before_normal = 0
awake_during_late = 0
awake_during_normal = 0


for i in range(len(df['24_hour'])):
    
    if df['date_year'][i]>= 2020 and df['date_month'][i] >= 3:
        if df['24_hour'][i] <= 6 or df['24_hour'][i] >= 23:
            awake_during_late += 1 
        else:
            awake_during_normal += 1
    else:
        if df['24_hour'][i] <= 6 or df['24_hour'][i] >= 23:
            awake_before_late += 1 
        else:
            awake_before_normal += 1       
        
print('awake_before_late: ', awake_before_late, 'awake_before_normal: ', awake_before_normal,
      'awake_during_late: ',awake_during_late, 'awake_during_normal: ', awake_during_normal)






""" Sleep Visualisations"""
## AUSTRALIA WIDE


import plotly.express as px

fig = px.histogram(df, x="clean_loc")
fig.write_html("location.html")

def numpyToSleepHist(aus_time):
    hist1 = go.Histogram(x=aus_time[aus_time<=6], 
                        opacity=0.75, 
                        marker_color='#E45756',
                        histnorm='density',
                        showlegend=False, nbinsx = 24
                        ) 
    hist2 = go.Histogram(x=aus_time[aus_time==23], 
                        opacity=0.75, 
                        marker_color='#E45756',
                        histnorm='density',
                        showlegend=False, nbinsx = 24
                        )
    hist3 = go.Histogram(x=aus_time[(aus_time>6) & (aus_time<23)], 
                        opacity=0.75, 
                        marker_color='#72B7B2',
                        histnorm='density',
                        showlegend=False, nbinsx = 24,  title=""
                        )                    
                        
    fig = go.Figure(data=[hist1, hist2,hist3])
    fig.update_yaxes(title = "Number of Tweets")
    fig.update_xaxes(title = "Time of tweets (24 hour)")
    return fig



BC_aus_time = before19_df['24_hour'].to_numpy()
DC_aus_time = during19_df['24_hour'].to_numpy()


fig_1 = numpyToSleepHist(BC_aus_time)
fig_1.update_layout(title="24 hour twitter activity before COVID19, Australia wide")
fig_1.update_yaxes(title = "Number of Tweets")
fig_1.update_xaxes(title = "Time of tweets (24 hour)")           
fig_1.write_html("Australia_awake_hist_BC.html")


fig_2 = numpyToSleepHist(DC_aus_time)
fig_2.update_layout(title="24 hour twitter activity during COVID19, Australia wide")
fig_2.update_yaxes(title = "Number of Tweets")
fig_2.update_xaxes(title = "Time of tweets (24 hour)") 
fig_2.write_html("Australia_awake_hist_DC.html")


status=['Standard Awake hours [7 - 22]', 'Late Awake hours [23 - 6]']

yBC = [awake_before_normal/(awake_before_normal+ awake_before_late), awake_before_late/(awake_before_normal+ awake_before_late)]
yDC = [awake_during_normal/(awake_during_normal+ awake_during_late), awake_during_late/(awake_during_normal+ awake_during_late)]

fig_3 = go.Figure(data=[
    go.Bar(name='Before COVID', x=status, y=yBC),
    go.Bar(name='During COVID', x=status, y=yDC)
])
# Change the bar mode
fig_3.update_layout(barmode='group')
fig_3.update_layout(title="Twitter activity before and after Covid")
fig_3.update_yaxes(title = "Preportion of Tweets")

fig_3.write_html("Australia_awake_total.html")

### By captial City
brisbane_df = df[df["clean_loc"] == 'brisbane']

fig_2 = px.histogram(brisbane_df, x="24_hour", nbins  = 24)
fig_2.write_html("brisbane_awake_hist.html")



"""Pets"""

text = df['text'][0]
count = 0
pet_set = set(['dog','cat','animal','vet','pet','chicken','lizard'])
pet_ind = []
pet_contains_emj_ind = []
for text in df['text']:
    text_emoj_free = emoji.demojize(text)
    if text == text_emoj_free:
        pet_contains_emj_ind.append(count)
    clean = text_emoj_free.translate(str.maketrans('', '', string.punctuation))
    tokens = set(clean.lower().split())
    for pet in pet_set:
        if pet in tokens:
            print(tokens)
            pet_ind.append(count)
    count += 1
       
pet_list=   [text_list[i] for i in pet_ind]




""" Pet Visualisations"""



"""Election""" 


count = 0
elect_set = set(['election','covid19','coronavirus','dictatordan','lockdown','labour','liberal','iso',
                 'bubble','covid normal' ,'isolation','premier','minister','draconian','crisis'])
elect_ind = []
elect_contains_emj_ind = []
for text in df['text']:
    text_emoj_free = emoji.demojize(text)
    if text != text_emoj_free:
        elect_contains_emj_ind.append(count)
    clean = text_emoj_free.translate(str.maketrans('', '', string.punctuation))
    tokens = (clean.lower().split())
    for token in tokens:
        if token in elect_set:
            
            elect_ind.append(count)
    count += 1
    
elect_text=   [text_list[i] for i in elect_ind]    
    
    
    

""" Election Visualisations"""    