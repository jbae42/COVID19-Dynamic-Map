import numpy as np 
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import PIL
import io

df = pd.read_csv('confirmed_US.csv')

drop_states = ['American Samoa','Diamond Princess','Grand Princess','Northern Mariana Islands','Puerto Rico']

df['Province_State'] = df['Province_State'].apply(lambda x: x if x not in drop_states else 0)

df['Province_State'] = df['Province_State'][df['Province_State'] != 0]


df1 = df.groupby('Province_State').sum()
df1 = df1.drop(columns=['UID','code3','FIPS','Lat','Long_'])


df_tr = df1.T

df_sum = df_tr.sum().sort_values(ascending=False)[:10]
df_sum.index

plt.figure()
df_tr.plot(y=df_sum.index, use_index=True, figsize=(8,8), rot=45, title='US TOP 5 States with COVID-19 Confirmed Case Numbers')
plt.ylabel('# of Confirmed Cases of COVID19 (in Million)')
plt.show()


US = gpd.read_file(r'input/us-states-cartographic-boundary-shapefiles/cb_2016_us_state_500k.shp')

ax = US.plot()
ax.set_xlim(-140, -55)
ax.set_ylim(25, 50)
ax.plot(figsize=(5,5))

statelist = df_tr.columns.to_list()

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

df_tr2 = df_tr.rename(us_state_abbrev, axis=1) 

for index, row in df_tr2.T.iterrows():
    if index not in US['STUSPS'].to_list():
        print(index, ' is not in the list in shapefile')
    else:
        #print(index,'here')
        pass
    
df_fin = df_tr2.T

merge = US.join(df_fin, on = 'STUSPS', how = 'right')


import mapclassify

img_list = []


for dates in merge.columns.to_list()[10:16]:
    ax = merge.plot(column = dates,
               cmap = 'PuBu',
               figsize = (10,10),
               legend = True,
                scheme = 'user_defined',
                classification_kwds = {'bins':[100,1000,10000,100000,250000,500000]},
               edgecolor = 'black',
               linewidth = 0.4)
    ax.set_xlim(-140, -55)
    ax.set_ylim(25, 50)
    ax.plot(figsize=(5,5))
    ax.set_title("COVID-19 Confirmed Case Numbers in US on {}".format(dates), fontdict={'fontsize':20},pad=12.5)
    ax.set_axis_off()
    ax.get_legend().set_bbox_to_anchor((0.18,0.4))
    img=ax.get_figure()
    f = io.BytesIO()
    img.savefig(f, format = 'png',bbox_inches='tight')
    f.seek(0)
    img_list.append(PIL.Image.open(f))
    
    
img_list[0].save('Animated US COVID-19 Map.gif',format='GIF',
                append_images = img_list[1:],
                save_all = True, duration = 300,
                loop = 0)

f.close()



