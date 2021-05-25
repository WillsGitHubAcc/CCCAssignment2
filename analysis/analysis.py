"""
COMP90024 2021 Semester 2 Assignment 2
Group 52
William Lazarus Kevin Dean 834444 Melbourne, Australia
Kenneth Huynh 992680 Melbourne, Australia
Joel Kenna 995401 Melbourne, Australia
Quinten van der Leest 1135216 Melbourne, Australia
Walter Zhang 761994 Melbourne, Australia

"""

import json


import plotly.express as px
import pandas as pd    
import string
import plotly.graph_objects as go
import emoji
import numpy as np
import plotly.graph_objects as go
import couchdb
import time

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



with open('credentials1.json', encoding = 'utf-8') as f:
  creds = json.load(f)


couch = couchdb.client.Server("http://{duser}:{dpword}@172.26.128.237:{port}/".format(duser = creds['database']['user'], 
                              dpword = creds['database']['pword'], port = creds['database']['port']))
couch.resource.credentials = (creds['database']['user'], creds['database']['pword'])
db = couch['tweets']


def timetohour(gmt_time,loc):
    if loc == "Perth":
        hour = (gmt_time[3] + 9) % 24
    else:
    
        hour = (gmt_time[3] + 11) % 24
    
    return hour

# Extract data from tweets into lists


hour24_list = []
date_year = []
date_month = []
text_list = []
location = []


count = 0
data_list = []
for row in db.iterview('test_view/textview', 100, include_docs=False):
    
    gmt_time = time.gmtime(row['key'][0])
    hour24_list.append(timetohour(gmt_time,row['value'][3]))
    date_year.append((gmt_time[0]) )
    date_month.append((gmt_time[1]))
    text_list.append(row['value'][0])
    location.append(row['value'][3])
   

    
for row in db.iterview('test_view/sleepview', 5, include_docs=False):
    hour_array=(row['value']['hourarray'])
    
    
hour_ind = set(hour24_list)    

hour_ind = list(hour_ind)

    
"""Pre-Processing"""
if len(text_list ) - len(location) ==1:
    location.append('Darwin')

# plus 11 because we are +11 from GMT



d = {'24_hour' : hour24_list, 'date_year' : date_year, 'date_month' :date_month ,
     'text' : text_list, 'location' : location, 'clean_loc' : location}

df = pd.DataFrame(d)
df = df.dropna()
df =df.reset_index()
# seperate dataframe into before and during covid

idx = np.where((df['date_year']>= 2020) & (df['date_month'] >= 3) )

during19_df = df.loc[idx]
before19_df = df.drop(idx[0], axis=0)



plot_time = []
for i in range(len(df['date_year'])):
    
    plot_time.append(str(df['date_year'][i]) + '-'+  str(df['date_month'][i]))
    
df['plot_time'] = plot_time



df_vic = pd.read_csv('data_sleep.csv')

couch = couchdb.client.Server("http://{duser}:{dpword}@172.26.128.237:{port}/".format(duser = creds['database']['user'], 
                              dpword = creds['database']['pword'], port = creds['database']['port']))
couch.resource.credentials = (creds['database']['user'], creds['database']['pword'])

db_G = couch['graphs']







### Spread of data for report

fig = px.histogram(df, x="clean_loc")
fig.update_layout(title="Distirbution of tweets")
fig.update_xaxes(title = "City")  
fig.write_json("location.json")
with open('location.json', encoding = 'utf-8') as f:
  location = json.load(f)
 
    
total_24_spread = px.bar(x=hour_ind , y=hour_array)
total_24_spread.update_layout(title="Time distirbution of tweets")
total_24_spread.update_xaxes(title = "24 hour time")  
total_24_spread.write_html("total_24_spread.html")  
  
doc = db_G.get("scenario_homepage")
if doc:
   doc["location"] = location
   
#Edit the doc:
else:
     doc = {"location":location,  '_id':'scenario_homepage'}
db_G.save(doc)








"""VICTORIA VISUALISATION"""
ind_v = [159,130,13,16,62,141]
df_v= df_vic.loc[ind_v]  

df_v[" estimate"] = df_v[" estimate"]/100

fig_sleep_vic = px.bar(df_v, x=" sla_name06", y=" estimate", range_y=[0,1],color_discrete_sequence=['indianred','indianred','indianred','indianred','indianred','indianred'])
fig_sleep_vic.update_layout(title="Sleep quality Victoria")
fig_sleep_vic.update_yaxes(title = "Preportion of residents that do not get adqeuate sleep <7 hours")
fig_sleep_vic.update_xaxes(title = "Victorian cities")  
#fig_sleep_vic.update_layout(showlegend=False)    
fig_sleep_vic.write_json("Victoria_sleep_study_AURIN.json")
with open('Victoria_sleep_study_AURIN.json', encoding = 'utf-8') as f:
  Victoria_sleep_study_AURIN = json.load(f)


"""SLEEP"""

def sleep_total(df):
    good_sleep = {}
    bad_sleep = {}
    
    for i in range(len(df['24_hour'])):
        
            
            if df['24_hour'][i] <= 6 or df['24_hour'][i] >= 23:
                if df['plot_time'][i] in bad_sleep.keys():
                    bad_sleep[df['plot_time'][i]] += 1
                else:
                    bad_sleep[df['plot_time'][i]] = 1
            else:
                if df['plot_time'][i] in good_sleep.keys():
                    good_sleep[df['plot_time'][i]] += 1
                else:
                    good_sleep[df['plot_time'][i]] = 1
            
    good_val =[]
    good_id =[]
    bad_val =[]
    bad_id =[]
    for key in good_sleep.keys():
        good_id.append(key)
        good_val.append(good_sleep[key])
        if key in bad_sleep.keys():
            bad_id.append(key)
            bad_val.append(bad_sleep[key])  
        else:
            bad_id.append(key)
            bad_val.append(0)
    
    
    d = {'id' :good_id, 'good_val' : good_val, "bad_val" : bad_val}
    
    
    
    
    df_Ssleep = pd.DataFrame(d)
    good_prep = []
    bad_prep = []
    for i in range(len(df_Ssleep['id'])):
        
        good_prep.append(df_Ssleep['good_val'][i]/(df_Ssleep['good_val'][i]+df_Ssleep['bad_val'][i])        )
        bad_prep.append(df_Ssleep['bad_val'][i]/(df_Ssleep['good_val'][i]+df_Ssleep['bad_val'][i]) )
    
    
    good_prep = good_prep + bad_prep    
    good_col =  ['Recommended amount of sleep'] * len(good_id)
    bad_coll = ['insufficent sleep']*len(good_id)
    good_col = good_col + bad_coll
    
    good_id = good_id+ bad_id
    good_val = good_val+bad_val
    
    
    d = {'id' :good_id, 'good_val' : good_val, "good_col" : good_col, 'good_prep':good_prep}
    
    df_Ssleep_2 = pd.DataFrame(d)
    return df_Ssleep_2




""" Sleep Visualisations"""
## AUSTRALIA WIDE

df_sleep = sleep_total(df)
   
        
fig_sleep1 = px.bar(df_sleep, x="good_col", y="good_prep", color = "good_col",
      animation_frame="id", animation_group="good_prep", range_y=[0,1])
       
    
fig_sleep1.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_sleep1.update_layout(title="Sleep quality Australia wide")
fig_sleep1.update_yaxes(title = "Preportion of Twitter users")
fig_sleep1.update_xaxes(title = "Sleep quality")  
fig_sleep1.update_layout(showlegend=False)    
fig_sleep1.write_json("aus_sleep_time.json")
with open('aus_sleep_time.json', encoding = 'utf-8') as f:
  aus_sleep_time = json.load(f)




brisbane_df = df[df["clean_loc"] == 'Brisbane']
brisbane_df = brisbane_df.reset_index()

adelaide_df = df[df["clean_loc"] == 'Adelaide']
adelaide_df = adelaide_df.reset_index()

melbourne_df = df[df["clean_loc"] == 'Melbourne']
melbourne_df = melbourne_df.reset_index()

perth_df = df[df["clean_loc"] == 'Perth']
perth_df = perth_df.reset_index()

hobart_df = df[df["clean_loc"] == 'Hobart']
hobart_df = hobart_df.reset_index()
canberra_df = df[df["clean_loc"] == 'Canberra']
canberra_df = canberra_df.reset_index()
darwin_df = df[df["clean_loc"] == 'Darwin']
darwin_df = darwin_df.reset_index()

sydney_df = df[df["clean_loc"] == 'Sydney']
sydney_df = sydney_df.reset_index()


brisbane_sleep = sleep_total(brisbane_df)
  
fig_sleepb = px.bar(df_sleep, x="good_col", y="good_prep", color = "good_col",
      animation_frame="id", animation_group="good_prep", range_y=[0,1])
 
fig_sleepb.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_sleepb.update_layout(title="Sleep quality Brisbane")
fig_sleepb.update_yaxes(title = "Preportion of Twitter users")
fig_sleepb.update_xaxes(title = "Sleep quality")  
fig_sleepb.update_layout(showlegend=False)  
fig_sleepb.write_json("bris_sleep_time.json")
with open('bris_sleep_time.json', encoding = 'utf-8') as f:
  bris_sleep_time = json.load(f)
  
  
  
adelaide_sleep = sleep_total(adelaide_df)
 
fig_sleepa = px.bar(df_sleep, x="good_col", y="good_prep", color = "good_col",
     animation_frame="id", animation_group="good_prep", range_y=[0,1])
   
fig_sleepa.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_sleepa.update_layout(title="Sleep quality Adelaide")
fig_sleepa.update_yaxes(title = "Preportion of Twitter users")
fig_sleepa.update_xaxes(title = "Sleep quality")  
fig_sleepa.update_layout(showlegend=False)    
fig_sleepa.write_json("adel_sleep_time.json")
with open('adel_sleep_time.json', encoding = 'utf-8') as f:
  adel_sleep_time = json.load(f)


melbourne_sleep = sleep_total(melbourne_df)
  
fig_sleepM = px.bar(melbourne_sleep, x="good_col", y="good_prep", color = "good_col",
     animation_frame="id", animation_group="good_prep", range_y=[0,1])
       
    
fig_sleepM.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_sleepM.update_layout(title="Sleep quality Melbourne")
fig_sleepM.update_yaxes(title = "Preportion of Twitter users")
fig_sleepM.update_xaxes(title = "Sleep quality")  
fig_sleepM.update_layout(showlegend=False)    
fig_sleepM.write_json("melb_sleep_time.json")
fig_sleepM.write_html("melb_sleep_time.html")
with open('melb_sleep_time.json', encoding = 'utf-8') as f:
  melb_sleep_time = json.load(f)

perth_sleep = sleep_total(perth_df)
  
fig_sleepP = px.bar(perth_sleep, x="good_col", y="good_prep", color = "good_col",
     animation_frame="id", animation_group="good_prep", range_y=[0,1])  
    
fig_sleepP.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_sleepP.update_layout(title="Sleep quality Perth")
fig_sleepP.update_yaxes(title = "Preportion of Twitter users")
fig_sleepP.update_xaxes(title = "Sleep quality")  
fig_sleepP.update_layout(showlegend=False)
fig_sleepP.write_json("perth_sleep_time.json")
with open('perth_sleep_time.json', encoding = 'utf-8') as f:
  perth_sleep_time = json.load(f)


hobart_sleep = sleep_total(hobart_df)
fig_sleeph = px.bar(hobart_sleep, x="good_col", y="good_prep", color = "good_col",
     animation_frame="id", animation_group="good_prep", range_y=[0,1])
    
fig_sleeph.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_sleeph.update_layout(title="Sleep quality Hobart")
fig_sleeph.update_yaxes(title = "Preportion of Twitter users")
fig_sleeph.update_xaxes(title = "Sleep quality")  
fig_sleeph.update_layout(showlegend=False)
fig_sleeph.write_json("hobart_sleep_time.json")
with open('hobart_sleep_time.json', encoding = 'utf-8') as f:
  hobart_sleep_time = json.load(f)


canberra_sleep = sleep_total(canberra_df)
fig_sleepc = px.bar(canberra_sleep, x="good_col", y="good_prep", color = "good_col",
     animation_frame="id", animation_group="good_prep", range_y=[0,1])
       
    
fig_sleepc.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_sleepc.update_layout(title="Sleep quality Canberra")
fig_sleepc.update_yaxes(title = "Preportion of Twitter users")
fig_sleepc.update_xaxes(title = "Sleep quality")  
fig_sleepc.update_layout(showlegend=False)
fig_sleepc.write_json("canberra_sleep_time.json")
with open('canberra_sleep_time.json', encoding = 'utf-8') as f:
  canberra_sleep_time = json.load(f)


darwin_sleep = sleep_total(darwin_df)
fig_sleepd = px.bar(darwin_sleep, x="good_col", y="good_prep", color = "good_col",
     animation_frame="id", animation_group="good_prep", range_y=[0,1])
       
    
fig_sleepd.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_sleepd.update_layout(title="Sleep quality Darwin")
fig_sleepd.update_yaxes(title = "Preportion of Twitter users")
fig_sleepd.update_xaxes(title = "Sleep quality")  
fig_sleepd.update_layout(showlegend=False)
fig_sleepd.write_json("darwin_sleep_time.json")
with open('darwin_sleep_time.json', encoding = 'utf-8') as f:
  darwin_sleep_time = json.load(f)


sydney_df_sleep = sleep_total(sydney_df)
fig_sleeps = px.bar(sydney_df_sleep, x="good_col", y="good_prep", color = "good_col",
     animation_frame="id", animation_group="good_prep", range_y=[0,1])
       
    
fig_sleepd.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_sleeps.update_layout(title="Sleep quality Sydney")
fig_sleeps.update_yaxes(title = "Preportion of Twitter users")
fig_sleeps.update_xaxes(title = "Sleep quality")  
fig_sleeps.update_layout(showlegend=False)
fig_sleeps.write_json("sydney_sleep_time.json")
with open('sydney_sleep_time.json', encoding = 'utf-8') as f:
  sydney_sleep_time = json.load(f)



"""EXPORT TO COUCHDB"""
  
doc = db_G.get("scenario_sleep")
if doc:
   doc["sydney_sleep_time"] = sydney_sleep_time
   doc["darwin_sleep_time"] = darwin_sleep_time
   doc['canberra_sleep_time'] = canberra_sleep_time
   doc['perth_sleep_time'] = perth_sleep_time
   doc['melb_sleep_time'] = melb_sleep_time
   doc['adel_sleep_time'] = adel_sleep_time
   doc['bris_sleep_time'] = bris_sleep_time
   doc['hobart_sleep_time'] = hobart_sleep_time
   doc['aus_sleep_time'] = aus_sleep_time
   doc['Victoria_sleep_study_AURIN'] = Victoria_sleep_study_AURIN
    
   
#Edit the doc:
else:
     doc = {"sydney_sleep_time":sydney_sleep_time, 'darwin_sleep_time':darwin_sleep_time, 'canberra_sleep_time':canberra_sleep_time,
       'hobart_sleep_time':hobart_sleep_time, 'perth_sleep_time':perth_sleep_time, 'melb_sleep_time':melb_sleep_time,
       'adel_sleep_time' :adel_sleep_time,
        'bris_sleep_time':bris_sleep_time,'aus_sleep_time':aus_sleep_time,
        'Victoria_sleep_study_AURIN': Victoria_sleep_study_AURIN, '_id':'scenario_sleep'}
db_G.save(doc)

"""Sentiment"""

plot_time = []
for i in range(len(df['date_year'])):
    
    plot_time.append(df['date_year'][i]*10 + df['date_month'][i])
    
df['plot_time'] = plot_time

PP_time = set(plot_time)

PP_city = set(df['clean_loc'])
df_sentiment = df.groupby(['plot_time','clean_loc']).mean()
city = []
plot_T= []
for index in df_sentiment.index:
    city.append(index[1])
    plot_T.append(index[0])
    
df_sentiment['city'] = city
df_sentiment['plot_T'] = plot_T


"""Pets"""



"""SA PET DATA"""

df_dog = pd.read_csv('data_dog.csv')

sum_nD_19 = df_dog['num_dogs_2019'].sum()
sum_nC_19 = df_dog[' num_cats_2019'].sum()
sum_nD_20 = df_dog[' num_dogs_2020'].sum()
sum_nC_20 = df_dog[' num_cats_2020'].sum()

D_per_ch = 100*(sum_nD_20 - sum_nD_19)/sum_nD_19 
C_per_ch = 100*(sum_nC_20 - sum_nC_19)/sum_nC_19 
m = (D_per_ch + C_per_ch)/2
vals = [C_per_ch,D_per_ch, m ]
name = ['cats','Dogs',"mean"]

fig_sa_dog = px.bar(x=name, y=vals)    
fig_sa_dog.update_layout(title="Percentage increase in Cat and Dog registration in SA (2019 - 2020)")
fig_sa_dog.update_yaxes(title = "% increase")
fig_sa_dog.write_json("sa_cats_dogs_AURIN.json")
with open('sa_cats_dogs_AURIN.json', encoding = 'utf-8') as f:
  sa_cats_dogs_AURIN = json.load(f)


"""TWeet Pet data"""
count = 0
pet_set = set(['dog','cat','animal','vet','pet','chicken','lizard'])
pet_ind = []
pet_contains_emj_ind = []
for text in df['text']:
    text_emoj_free = emoji.demojize(text)
    
    clean = text_emoj_free.translate(str.maketrans('', '', string.punctuation))
    tokens = set(clean.lower().split())
    for pet in pet_set:
        if pet in tokens:
           pet_ind.append(count)
    count += 1
       


df_pet= df.loc[pet_ind]   
df_pet = df_pet.reset_index()

P_idx = np.where((df_pet['date_year']>= 2020) & (df_pet['date_month'] >= 3) )


petduring19_df = df_pet.loc[P_idx]
petbefore19_df = df_pet.drop(P_idx[0], axis=0)

during_count = petduring19_df.groupby("location").count()
before_count = petbefore19_df.groupby("location").count()
p_city = []
during_list = []
before_list = []


for city in during_count.index:
    
    during_list.append(during_count['24_hour'][city])
    if city in before_count.index:
        before_list.append(before_count['24_hour'][city])
    else:
        before_list.append(0)
    p_city.append(city)

    
per_change = []

for i in range(len(during_list)):
    per_change.append(100*(during_list[i] - before_list[i])/during_list[i] )

""" Pet Visualisations"""

fig_aus_pet = px.bar(x=p_city, y=per_change)    
fig_aus_pet.update_layout(title="Percentage Change in Pet tweets before and during COVID")
fig_aus_pet.update_yaxes(title = "% change")
fig_aus_pet.write_json("aus_pet.json")
with open('aus_pet.json', encoding = 'utf-8') as f:
  aus_pet = json.load(f)


x_p = ['Number of pet tweet before Covid', 'Number of pet tweets after Covid', 'Percentage change in tweets']

value = []
val_dict = {}
for city in p_city:
    ind = p_city.index(city)
    value = []
    value.append(before_list[ind])
    value.append(during_list[ind])
    value.append(per_change[ind])
    
    val_dict[city] = (value)    


fig_adel_pet = px.bar(x=x_p, y=val_dict['Adelaide'])    
fig_adel_pet.update_layout(title="Change in pet tweets before and during Covid Adelaide")
fig_adel_pet.update_yaxes(title = "Change")
fig_adel_pet.write_json("adel_pet.json")
with open('adel_pet.json', encoding = 'utf-8') as f:
  adel_pet = json.load(f)

fig_bris_pet = px.bar(x=x_p, y=val_dict['Brisbane'])    
fig_bris_pet.update_layout(title="Change in pet tweets before and during Covid Brisbane")
fig_bris_pet.update_yaxes(title = "Change")
fig_bris_pet.write_json("bris_pet.json")
with open('bris_pet.json', encoding = 'utf-8') as f:
  bris_pet = json.load(f)

fig_canb_pet = px.bar(x=x_p, y=val_dict['Canberra'])    
fig_canb_pet.update_layout(title="Change in pet tweets before and during Covid Canberra")
fig_canb_pet.update_yaxes(title = "Change")
fig_canb_pet.write_json("canb_pet.json")
with open('canb_pet.json', encoding = 'utf-8') as f:
  canb_pet = json.load(f)
  
fig_darw_pet = px.bar(x=x_p, y=val_dict['Darwin'])    
fig_darw_pet.update_layout(title="Change in pet tweets before and during Covid Darwin")
fig_darw_pet.update_yaxes(title = "Change")
fig_darw_pet.write_json("darwin_pet.json")
with open('darwin_pet.json', encoding = 'utf-8') as f:
  darwin_pet = json.load(f)

fig_Hoba_pet = px.bar(x=x_p, y=val_dict['Hobart'])    
fig_Hoba_pet.update_layout(title="Change in pet tweets before and during Covid Hobart")
fig_Hoba_pet.update_yaxes(title = "Change")
fig_Hoba_pet.write_json("hobart_pet.json")
with open('hobart_pet.json', encoding = 'utf-8') as f:
  hobart_pet = json.load(f)
  
  
fig_melb_pet = px.bar(x=x_p, y=val_dict['Melbourne'])    
fig_melb_pet.update_layout(title="Change in pet tweets before and during Covid Melbourne")
fig_melb_pet.update_yaxes(title = "Change")
fig_melb_pet.write_json("melb_pet.json")
with open('melb_pet.json', encoding = 'utf-8') as f:
  melb_pet = json.load(f)
  
fig_perth_pet = px.bar(x=x_p, y=val_dict['Perth'])    
fig_perth_pet.update_layout(title="Change in pet tweets before and during Covid Perth")
fig_perth_pet.update_yaxes(title = "Change")
fig_perth_pet.write_json("perth_pet.json")
with open('perth_pet.json', encoding = 'utf-8') as f:
  perth_pet = json.load(f)

fig_Sydney_pet = px.bar(x=x_p, y=val_dict['Sydney'])    
fig_Sydney_pet.update_layout(title="Change in pet tweets before and during Covid Sydney")
fig_Sydney_pet.update_yaxes(title = "Change")
fig_Sydney_pet.write_json("Sydney_pet.json")
with open('Sydney_pet.json', encoding = 'utf-8') as f:
  sydney_pet = json.load(f)

  
"""EXPORT TO COUCHDB"""
  
doc = db_G.get("scenario_pet")
if doc:
   doc["sydney_pet"] = sydney_pet
   doc["perth_pet"] = perth_pet
   doc['melb_pet'] = melb_pet
   doc['hobart_pet'] = hobart_pet
   doc['darwin_pet'] = darwin_pet
   doc['canb_pet'] = canb_pet
   doc['bris_pet'] = bris_pet
   doc['adel_pet'] = adel_pet
   doc['aus_pet'] = aus_pet
   doc['sa_cats_dogs_AURIN'] = sa_cats_dogs_AURIN
   
#Edit the doc:
else:
     doc = {"sydney_pet":sydney_pet, 'perth_pet':perth_pet, 'melb_pet':melb_pet,
       'hobart_pet':hobart_pet, 'darwin_pet':darwin_pet, 'canb_pet':canb_pet, 'bris_pet' :bris_pet,
        'adel_pet':adel_pet,'aus_pet':aus_pet,'sa_cats_dogs_AURIN': sa_cats_dogs_AURIN, '_id':'scenario_pet'}
db_G.save(doc)




"""Election""" 
## FOR Labour, against labour
## For liberial, against liberal
"""AURIN Election 2019""" 

df_2pp = pd.read_csv('data_elect_19.csv')

df_mean_2pp = df_2pp.groupby(' state').mean()



elect19_fig = go.Figure(data=[
    go.Bar(name='Liberial mean vote % (2pp)', x=df_mean_2pp.index, y=df_mean_2pp[' tpp_liberal_national_coalition_percentage']),
    go.Bar(name='Labour mean vote % (2pp)', x=df_mean_2pp.index, y=df_mean_2pp['tpp_australian_labor_party_percentage'])
])
# Change the bar mode
elect19_fig.update_layout(barmode='group')
elect19_fig.update_layout(title="2 party preferred votes for 2019 Australian election (mean)")
elect19_fig.update_yaxes(title = "Mean vote %")

elect19_fig.write_json("elect19_2pp_AURIN.json")
with open('elect19_2pp_AURIN.json', encoding = 'utf-8') as f:
  elect19_2pp_AURIN = json.load(f)


"""Twitter Election""" 
count = 0
elect_set = set(['election','covid19','coronavirus','Gladys' ,'Berejiklian','Daniel','Andrews',
                 'lockdown','labour','liberal','iso', "Mark","McGowan",
                 'bubble','covid normal' ,'isolation','premier','minister','draconian','crisis'])
elect_ind = []
elect_contains_emj_ind = []
for text in df['text']:
    text_emoj_free = emoji.demojize(text)
    
    clean = text_emoj_free.translate(str.maketrans('', '', string.punctuation))
    tokens = set(clean.lower().split())
    for token in tokens:
        if token in elect_set:
            
            elect_ind.append(count)
    count += 1
    

df_elect = df.loc[elect_ind]   
df_elect = df_elect.reset_index()
loc_set =  set(df_elect['clean_loc'])


sentiment_score = []
for text in df_elect['text']:
    
    score = SentimentIntensityAnalyzer().polarity_scores(emoji.demojize(text))
    sentiment_score.append(score['compound'])

df_elect['sentiment'] = sentiment_score

E_idx = np.where((df_elect['date_year']>= 2020) & (df_elect['date_month'] >= 3) )


electduring19_df = df_elect.loc[E_idx]
electbefore19_df = df_elect.drop(E_idx[0], axis=0)

before_good_dict = {}
before_bad_dict = {}
during_bad_dict = {}
during_good_dict = {}

for i in electbefore19_df.index:
    
    if electbefore19_df['sentiment'][i] >= 0:
        if electbefore19_df['clean_loc'][i] in before_good_dict.keys():
            before_good_dict[electbefore19_df['clean_loc'][i]] += 1
        else:
            before_good_dict[electbefore19_df['clean_loc'][i]] = 1 
    else:
        if electbefore19_df['clean_loc'][i] in before_bad_dict.keys():
            before_bad_dict[electbefore19_df['clean_loc'][i]] += 1
        else:
            before_bad_dict[electbefore19_df['clean_loc'][i]] = 1 
        
for i in electduring19_df.index:
    
    if electduring19_df['sentiment'][i] >= 0:
        if electduring19_df['clean_loc'][i] in during_good_dict.keys():
            during_good_dict[electduring19_df['clean_loc'][i]] += 1
        else:
            during_good_dict[electduring19_df['clean_loc'][i]] = 1 
    else:
        if electduring19_df['clean_loc'][i] in during_bad_dict.keys():
            during_bad_dict[electduring19_df['clean_loc'][i]] += 1
        else:
            during_bad_dict[electduring19_df['clean_loc'][i]] = 1         

val = []
sentiment = []
before = []
city_l = []
for city in loc_set:
    if city in before_good_dict.keys():
        val.append(before_good_dict[city])
        sentiment.append('Positive')    
        before.append('Before COVID')
        city_l.append(city)
    else:
        val.append(0)
        sentiment.append('Positive')    
        before.append('Before COVID')
        city_l.append(city)
val_3 = []
sentiment_3 = []
before_3 = []
city_l_3 = []        
        
for city in loc_set:
    if city in before_bad_dict.keys():
        val_3.append(before_bad_dict[city])
        sentiment_3.append('Negative')    
        before_3.append('Before COVID')
        city_l_3.append(city)
    else:
        val_3.append(0)
        sentiment_3.append('Negative')    
        before_3.append('Before COVID')
        city_l_3.append(city)    
        
val_2 = []
sentiment_2 = []
before_2 = []
city_l_2 = []        
for city in loc_set:
    if city in during_good_dict.keys():
        val_2.append(during_good_dict[city])
        sentiment_2.append('Positive')    
        before_2.append('During COVID')
        city_l_2.append(city)
    else:
        val_2.append(0)
        sentiment_2.append('Positive')    
        before_2.append('During COVID')
        city_l_2.append(city)    
        
val_4 = []
sentiment_4 = []
before_4 = []
city_l_4 = []        
for city in loc_set:
    if city in during_bad_dict.keys():
        val_4.append(during_bad_dict[city])
        sentiment_4.append('Negative')    
        before_4.append('During COVID')
        city_l_4.append(city)
    else:
        val_4.append(0)
        sentiment_4.append('Negative')    
        before_4.append('During COVID')
        city_l_4.append(city)    
    


""" Election Visualisations"""    





fig_elect_1 = go.Figure(data=[
    go.Bar(name='Postive Before Covid', x=city_l, y=val),
    go.Bar(name='Positive During Covid', x=city_l, y=val_2),
    go.Bar(name='Negatve Before Covid', x=city_l, y=val_3),
    go.Bar(name='Negative During Covid', x=city_l, y=val_4)])

    
# Change the bar mode
fig_elect_1.update_layout(barmode='group')

fig_elect_1.update_layout(title="Politcal sentiment before and during COVID Australia wide")
fig_elect_1.update_yaxes(title = "Number of political tweets")
  
fig_elect_1.write_json("Aus_elect.json")  
with open('Aus_elect.json', encoding = 'utf-8') as f:
  aus_elect = json.load(f) 



t = ['Postive Before Covid','Positive During Covid','Negatve Before Covid','Negative During Covid']
value = []
val_dict = {}
for city in city_l:
    ind = city_l.index(city)
    value = []
    value.append(val[ind])
    value.append(val_2[ind])
    value.append(val_3[ind])
    value.append(val_4[ind])
    val_dict[city] = (value)  
      
color = ['Positive','Positive','Negative','Negative']
fig_elect_2 = px.bar(x=t, y=val_dict['Brisbane'], color = color)    
fig_elect_2.update_layout(title="Politcal sentiment before and during COVID Brisbane")
fig_elect_2.update_yaxes(title = "Number of political tweets")
fig_elect_2.write_json("bris_elect.json")
with open('bris_elect.json', encoding = 'utf-8') as f:
  bris_elect = json.load(f) 

fig_elect_2 = px.bar(x=t, y=val_dict['Darwin'], color = color)    
fig_elect_2.update_layout(title="Politcal sentiment before and during COVID Brisbane")
fig_elect_2.update_yaxes(title = "Number of political tweets")
fig_elect_2.write_json("darwin_elect.json")
with open('darwin_elect.json', encoding = 'utf-8') as f:
  darwin_elect = json.load(f) 




fig_elect_3 = px.bar(x=t, y=val_dict['Adelaide'],color = color)    
fig_elect_3.update_layout(title="Politcal sentiment before and during COVID Adelaide")
fig_elect_3.update_yaxes(title = "Number of political tweets")
fig_elect_3.write_json("adel_elect.json")
with open('adel_elect.json', encoding = 'utf-8') as f:
  adel_elect = json.load(f) 


fig_elect_4 = px.bar(x=t, y=val_dict['Melbourne'],color = color)    
fig_elect_4.update_layout(title="Politcal sentiment before and during COVID Melbourne")
fig_elect_4.update_yaxes(title = "Number of political tweets")
fig_elect_4.write_json("melb_elect.json")
with open('melb_elect.json', encoding = 'utf-8') as f:
  melb_elect = json.load(f) 
  
  
fig_elect_5 = px.bar(x=t, y=val_dict['Perth'],color = color)    
fig_elect_5.update_layout(title="Politcal sentiment before and during COVID Perth")
fig_elect_5.update_yaxes(title = "Number of political tweets")
fig_elect_5.write_json("perth_elect.json")
with open('perth_elect.json', encoding = 'utf-8') as f:
  perth_elect = json.load(f) 
  
fig_elect_6 = px.bar(x=t, y=val_dict['Sydney'],color = color)    
fig_elect_6.update_layout(title="Politcal sentiment before and during COVID Sydney")
fig_elect_6.update_yaxes(title = "Number of political tweets")
fig_elect_6.write_json("sydney_elect.json")
with open('sydney_elect.json', encoding = 'utf-8') as f:
  sydney_elect = json.load(f) 

fig_elect_7 = px.bar(x=t, y=val_dict['Canberra'],color = color)    
fig_elect_7.update_layout(title="Politcal sentiment before and during COVID Canberra")
fig_elect_7.update_yaxes(title = "Number of political tweets")
fig_elect_7.write_json("canberra_elect.json")
with open('canberra_elect.json', encoding = 'utf-8') as f:
  canberra_elect = json.load(f) 
  
fig_elect_7 = px.bar(x=t, y=val_dict['Hobart'],color = color)    
fig_elect_7.update_layout(title="Politcal sentiment before and during COVID Hobart")
fig_elect_7.update_yaxes(title = "Number of political tweets")
fig_elect_7.write_json("Hobart_elect.json")
with open('Hobart_elect.json', encoding = 'utf-8') as f:
  hobart_elect = json.load(f)
  
  
"""EXPORT TO COUCHDB"""
  
doc = db_G.get("scenario_elect")
if doc:
   doc["hobart_elect"] = hobart_elect
   doc["canberra_elect"] = canberra_elect
   doc['sydney_elect'] = sydney_elect
   doc['perth_elect'] = perth_elect
   doc['melb_elect'] = melb_elect
   doc['adel_elect'] = adel_elect
   doc['darwin_elect'] = darwin_elect
   doc['bris_elect'] = bris_elect
   doc['aus_elect'] = aus_elect
   doc['elect19_2pp_AURIN'] = elect19_2pp_AURIN
   
#Edit the doc:
else:
     doc = {"hobart_elect":hobart_elect, 'canberra_elect':canberra_elect, 'sydney_elect':sydney_elect,
       'perth_elect':perth_elect, 'melb_elect':melb_elect, 'adel_elect':adel_elect, 'darwin_elect' :darwin_elect,
        'bris_elect':bris_elect,'aus_elect':aus_elect,'elect19_2pp_AURIN': elect19_2pp_AURIN, '_id':'scenario_elect'}
db_G.save(doc)




