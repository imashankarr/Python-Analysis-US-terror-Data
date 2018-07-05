import numpy as np
import pandas as pd
from plotly.offline import iplot
import plotly.offline
import plotly.plotly as py
import plotly 
from plotly import tools

import plotly.graph_objs as go



##Load the csv file
us_terror_info = pd.read_csv('C:\\Users\\imash\\OneDrive\\Desktop\\gtd\\usTerrorData.csv', encoding='ISO-8859-1', usecols=[0, 1, 2, 3, 8, 11, 13, 14, 35, 84, 100, 103])

#rename the columns
us_terror_info.rename(columns={'eventid':'id','iyear':'year','imonth':'month', 'iday':'day','country_txt':'country', 'provstate':'state', 'targtype1_txt':'target','weapsubtype1_txt':'weapon', 'nkillter':'fatalities', 'nwoundte':'injuries'}, inplace=True)

#datatype conversion 
us_terror_info['fatalities'] = us_terror_info['fatalities'].fillna(0).astype(int)
us_terror_info['injuries'] = us_terror_info['injuries'].fillna(0).astype(int)


us_terror_info = us_terror_info[(us_terror_info.country == 'United States') &
                         (us_terror_info.state != 'Puerto Rico') &
                         (us_terror_info.longitude < 0)]
us_terror_info['day'][us_terror_info.day == 0] = 1
us_terror_info['date'] = pd.to_datetime(us_terror_info[['day', 'month', 'year']])
us_terror_info = us_terror_info[['id', 'date', 'year', 'state', 'latitude', 'longitude',
                         'target', 'weapon', 'fatalities', 'injuries']]
us_terror_info = us_terror_info.sort_values(['fatalities', 'injuries'], ascending = False)
us_terror_info = us_terror_info.drop_duplicates(['date', 'latitude', 'longitude', 'fatalities'])


#Terrorist Attacks by Latitude/Longitude in the United States

us_terror_info['text'] = us_terror_info['date'].dt.strftime('%B %-d, %Y') + '<br>' + \
                         us_terror_info['fatalities'].astype(str) + ' Killed, ' + \
                         us_terror_info['injuries'].astype(str) + ' Injured'

fatality = dict(
    type='scattergeo',
    locationmode='USA-states',
    lon=us_terror_info[us_terror_info.fatalities > 0]['longitude'],
    lat=us_terror_info[us_terror_info.fatalities > 0]['latitude'],
    text=us_terror_info[us_terror_info.fatalities > 0]['text'],
    mode='markers',
    name='Fatalities',
    hoverinfo='text+name',
    marker=dict(
        size=us_terror_info[us_terror_info.fatalities > 0]['fatalities'] ** 0.255 * 8,
        opacity=0.95,
        color='rgb(240, 140, 45)')
)

injury = dict(
    type='scattergeo',
    locationmode='USA-states',
    lon=us_terror_info[us_terror_info.fatalities == 0]['longitude'],
    lat=us_terror_info[us_terror_info.fatalities == 0]['latitude'],
    text=us_terror_info[us_terror_info.fatalities == 0]['text'],
    mode='markers',
    name='Injuries',
    hoverinfo='text+name',
    marker=dict(
        size=(us_terror_info[us_terror_info.fatalities == 0]['injuries'] + 1) ** 0.245 * 8,
        opacity=0.85,
        color='rgb(20, 150, 187)')
)

layout = dict(
    title='United States Terror Attacks from 1970 to 2015',
    showlegend=True,
    legend=dict(
        x=0.85, y=0.4
    ),
    geo=dict(
        scope='usa',
        projection=dict(type='albers usa'),
        showland=True,
        landcolor='rgb(250, 250, 250)',
        subunitwidth=1,
        subunitcolor='rgb(217, 217, 217)',
        countrywidth=1,
        countrycolor='rgb(217, 217, 217)',
        showlakes=True,
        lakecolor='rgb(255, 255, 255)')
)

data = [fatality, injury]
figure1 = dict(data=data, layout=layout)

plotly.offline.plot(figure1)



# terrorist attacks by year
attacksPerYear = np.asarray(us_terror_info.groupby('year').year.count())

years = np.arange(1970, 2016)
# terrorist attacks in 1993 missing from database
years = np.delete(years, [23])

trace = [go.Scatter(
         x = years,
         y = attacksPerYear,
         mode = 'lines',
         line = dict(
             color = 'rgb(240, 140, 45)',
             width = 3)
         )]

layout = go.Layout(
         title = 'Terrorist Attacks by Year in United States (1970-2015)',
         xaxis = dict(
             rangeslider = dict(thickness = 0.05),
             showline = True,
             showgrid = False
         ),
         yaxis = dict(
             range = [0.1, 425],
             showline = True,
             showgrid = False)
         )

figure2 = dict(data = trace, layout = layout)


plotly.offline.plot(figure2)



#Terrorist Attacks per Capita

states = np.asarray(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
                        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
                        'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                        'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                        'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])

# US state population according to US census 2015
population = np.asarray([4858979, 738432, 6828065, 2978204, 39144818, 5456574,
                               3590886, 945934, 646449, 20271272, 10214860, 1431603,
                               1654930, 12859995, 6619680, 3123899, 2911641, 4425092,
                               4670724, 1329328, 6006401, 6794422, 9922576, 5489594,
                               2992333, 6083672, 1032949, 1896190, 2890845, 1330608,
                               8958013, 2085109, 19795791, 10042802, 756927, 11613423,
                               3911338, 4028977, 12802503, 1056298, 4896146, 858469,
                               6600299, 27469114, 2995919, 626042, 8382993, 7170351,
                               1844128, 5771337, 586107])


# terrorist attacks per 100,000 people in state
perstate_terror = np.asarray(us_terror_info.groupby('state').state.count())
percapita_terror = np.round(perstate_terror / population * 100000, 2)
# District of Columbia outlier (1 terrorist attack per 10,000 people) adjusted
percapita_terror[8] = round(percapita_terror[8] / 6, 2)

terror_scale = [[0, 'rgb(252, 232, 213)'], [1, 'rgb(240, 140, 45)']]

data = [dict(
        type = 'choropleth',
        autocolorscale = False,
        colorscale = terror_scale,
        showscale = False,
        locations = states,
        locationmode = 'USA-states',
        z = percapita_terror,
        marker = dict(
            line = dict(
                color = 'rgb(255, 255, 255)',
                width = 4)
            )
        )]

layout = dict(
         title = 'Terrorist Attacks per Capita in United States',
         geo = dict(
             scope = 'usa',
             projection = dict(type = 'albers usa'),
             countrycolor = 'rgb(255, 255, 255)',
             showlakes = True,
             lakecolor = 'rgb(255, 255, 255)')
         )

figure = dict(data = data, layout = layout)

plotly.offline.plot(figure)
