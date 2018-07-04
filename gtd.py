import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly 
from plotly import tools
import plotly.offline
import plotly.graph_objs as go



#Load the csv file
us_terror_info = pd.read_csv('C:\\Users\\imash\\OneDrive\\Desktop\\gtd\\usTerrorData.csv', encoding='ISO-8859-1', usecols=[0, 1, 2, 3, 8, 11, 13, 14, 35, 84, 100, 103])

#rename the columns
us_terror_info.rename(columns={'eventid':'id','iyear':'year','imonth':'month', 'iday':'day','country_txt':'country', 'provstate':'state', 'targtype1_txt':'target','weapsubtype1_txt':'weapon', 'nkillter':'fatalities', 'nwoundte':'injuries'}, inplace=True)

#datatype conversion 
us_terror_info['fatalities'] = us_terror_info['fatalities'].fillna(0).astype(int)
us_terror_info['injuries'] = us_terror_info['injuries'].fillna(0).astype(int)


##Terrorist attack visualization on United States Map

print("terror attack by logi")

terror_usa['text'] = terror_usa['date'].dt.strftime('%B %-d, %Y') + '<br>' +\
                     terror_usa['fatalities'].astype(str) + ' Killed, ' +\
                     terror_usa['injuries'].astype(str) + ' Injured'

fatality = dict(
           type = 'scattergeo',
           locationmode = 'USA-states',
           lon = terror_usa[terror_usa.fatalities > 0]['longitude'],
           lat = terror_usa[terror_usa.fatalities > 0]['latitude'],
           text = terror_usa[terror_usa.fatalities > 0]['text'],
           mode = 'markers',
           name = 'Fatalities',
           hoverinfo = 'text+name',
           marker = dict(
               size = terror_usa[terror_usa.fatalities > 0]['fatalities'] ** 0.225 * 9,
               opacity = 0.90,
               color = 'rgb(230, 155, 55)')
           )
        
injury = dict(
         type = 'scattergeo',
         locationmode = 'USA-states',
         lon = terror_usa[terror_usa.fatalities == 0]['longitude'],
         lat = terror_usa[terror_usa.fatalities == 0]['latitude'],
         text = terror_usa[terror_usa.fatalities == 0]['text'],
         mode = 'markers',
         name = 'Injuries',
         hoverinfo = 'text+name',
         marker = dict(
             size = (terror_usa[terror_usa.fatalities == 0]['injuries'] + 1) ** 0.235 * 9,
             opacity = 0.85,
             color = 'rgb(30, 170, 197)')
         )

layout = dict(
         title = 'Terrorist Attacks Vizualization on the United States Maps',
         showlegend = True,
         legend = dict(
             x = 0.80, y = 0.5
         ),
         geo = dict(
             scope = 'usa',
             projection = dict(type = 'albers usa'),
             showland = True,
             landcolor = 'rgb(250, 250, 250)',
             subunitwidth = 1,
             subunitcolor = 'rgb(217, 217, 217)',
             countrywidth = 1,
             countrycolor = 'rgb(217, 217, 217)',
             showlakes = True,
             lakecolor = 'rgb(255, 255, 255)')
         )

data = [fatality, injury]
figure = dict(data = data, layout = layout)


#################
#plotly.offline.plot(figure)
################
# terrorist attacks by year
terror_peryear = np.asarray(terror_usa.groupby('year').year.count())

terror_years = np.arange(1970, 2016)
# terrorist attacks in 1993 missing from database
terror_years = np.delete(terror_years, [23])

trace = [go.Scatter(
         x = terror_years,
         y = terror_peryear,
         mode = 'lines',
         line = dict(
             color = 'rgb(240, 140, 45)',
             width = 3)
         )]

layout = go.Layout(
         title = 'Terrorist Attacks by Year in the US',
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

figure = dict(data = trace, layout = layout)
##################
#plotly.offline.plot(figure)
#############
#Attacks per capital
us_states = np.asarray(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
                        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
                        'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                        'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                        'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])

# state population estimates for July 2015 from US Census Bureau
state_population = np.asarray([4858979, 738432, 6828065, 2978204, 39144818, 5456574,
                               3590886, 945934, 646449, 20271272, 10214860, 1431603,
                               1654930, 12859995, 6619680, 3123899, 2911641, 4425092,
                               4670724, 1329328, 6006401, 6794422, 9922576, 5489594,
                               2992333, 6083672, 1032949, 1896190, 2890845, 1330608,
                               8958013, 2085109, 19795791, 10042802, 756927, 11613423,
                               3911338, 4028977, 12802503, 1056298, 4896146, 858469,
                               6600299, 27469114, 2995919, 626042, 8382993, 7170351,
                               1844128, 5771337, 586107])

# terrorist attacks per 100,000 people in state
terror_perstate = np.asarray(terror_usa.groupby('state').state.count())
terror_percapita = np.round(terror_perstate / state_population * 100000, 2)
# District of Columbia outlier (1 terrorist attack per 10,000 people) adjusted
terror_percapita[8] = round(terror_percapita[8] / 6, 2)

terror_scale = [[0, 'rgb(252, 232, 213)'], [1, 'rgb(240, 140, 45)']]

data = [dict(
        type = 'choropleth',
        autocolorscale = False,
        colorscale = terror_scale,
        showscale = False,
        locations = us_states,
        locationmode = 'USA-states',
        z = terror_percapita,
        marker = dict(
            line = dict(
                color = 'rgb(255, 255, 255)',
                width = 2)
            )
        )]

layout = dict(
         title = 'Attacks per Capita in the US',
         geo = dict(
             scope = 'usa',
             projection = dict(type = 'albers usa'),
             countrycolor = 'rgb(255, 255, 255)',
             showlakes = True,
             lakecolor = 'rgb(255, 255, 255)')
         )

figure = dict(data = data, layout = layout)

################
plotly.offline.plot(figure)
#################


