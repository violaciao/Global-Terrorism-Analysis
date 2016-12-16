'''
This module contains
    - Choropleth class, with attributes and methods
    - functions to process data in json file
    - functions to plot Choropleth map
    - functions to assist the plot

This module allows users to
    - select year
    - select the target feature
    - visualize the terror attacks' occurrences, casualties, deaths or wounds
    - customize color palette
    - zoom up to get a more detialed view

@author: Xianzhi Cao (xc965)
'''


import pandas as pd
import numpy as np
import folium
import data
import heatmap as ht
from ipywidgets import IntSlider, Dropdown, interact
from UserError import *


class Choropleth(object):
    '''
    Attributes:
        - self.Year
        - self.Feature: feature name (casualties / kills / wounds)
        - self.dy_by_yr:   all attack data in the selected year
    Method:
        - get the total number of chosen feature in the chosen year in all countries
        - get the max number of chosen feature
        - get the scale upper bound
        - merge the data with all the countrie listed in json file
    '''
    def __init__(self, Year, Feature):
        self.Year = Year
        self.Feature = Feature
        self.df_by_yr = data.df_year_idx().loc[Year].fillna(0)

    def damage_by_year(self):
        '''
        Return a grouped DataFrame of chosen Feature values
        by the countries in the given year.
        '''
        dam_df_yr = self.df_by_yr[['country', self.Feature]]
        return dam_df_yr.groupby(['country']).sum()

    def max_dam(self):
        '''
        Return the maximum value of the chosen Feature by the chosen year
        '''
        dam_series = self.damage_by_year()[self.Feature]
        return dam_series.max()

    def scale_max(self):
        '''
        Return the upper bound of the chosen feature for plotting
        '''
        return (int(self.max_dam() / 100) + 1) * 100


    def all_ctr_dam(self):
        '''
        merge all countries together
        fill "-99" if there was no attack in the chosen year
        '''
        dam_by_year = self.damage_by_year().reset_index()
        js_ctr = js_country_names()
        # mage a dataframe with all the countries in the world
        # fill the non-attack years with the number '-99'
        # to differentiate them from other years,
        # especially from zero-casualty years
        merged_df = pd.merge(dam_by_year, js_ctr, on='country', how='outer').fillna(-99)
        sorted_df = merged_df.sort_values(by='country')
        new_df = sorted_df.reset_index().drop('index', 1)  # reset the index after sorting
        return new_df


def find_js_country_names():
    '''
    load the geo json file
    get all the country names   |   numpy array
    '''
    j = data.load_json_file('countries.geo.json')
    ls = []
    for i in j['features']:
        ls.append(i['properties']['name'])
    return np.array(ls)


def js_country_names():
    '''
    Return all the names under the column "country"   |   DataFrame
    '''
    js_ctr = pd.DataFrame(find_js_country_names(), columns=['country'])
    return js_ctr


def plot_choropleth(Color, Feature, Year):
    '''
    Parameters
        - Color     : color palette         | str
        - Feature   : feature of damages    | str
        - Year      : between 1970-2015     | str
    Return
        A Choropleth Map: The darker the color for a country,
                          the more damages had taken place.
    '''
    # Catch the exceptions if the user chooses the year 1993.
    if int(Year) == 1993:
        print('Data of 1993 is not available in Global Terrorism Database.\n\
Click the link to learn why.\nhttps://www.start.umd.edu/gtd/faq/')

    # Catch the exceptions if the user chooses a year out of data range
    elif int(Year) not in range(1970, 2016):
        raise NoDataError
    else:
        gtd_data = Choropleth(Year, Feature).all_ctr_dam()
        world_geo = r'countries.geo.json'
        # The upper bound of scale bar
        up = Choropleth(Year, Feature).scale_max()
        # Set the map base
        map = folium.Map(location=[32, -90],
                         zoom_start=2,
                         min_zoom=2,
                         tiles='Mapbox bright')
        # choropleth map settings
        map.choropleth(geo_path=world_geo, data=gtd_data,
                       columns=['country', Feature],
                       threshold_scale=[0, 10, 100, up/3, up*2/3, up],
                       key_on='feature.properties.name',
                       fill_color=Color, fill_opacity=0.7, line_opacity=0.2,
                       legend_name='Damage Scale',  # folium is not supportive to show legend_name on python 3.5
                       reset=True
                       )
        return map


def year_slider():
    '''
    Return a year from ipywidgets' IntSlider by users' manual pick
    '''
    yr = IntSlider(value=2010,
                   min=1970,
                   max=2015,
                   step=1,
                   description='Year',
                   disabled=False,
                   continuous_update=False,
                   orientation='horizontal',
                   readout=True,
                   readout_format='i',
                   slider_color='white'
                   )
    yr.layout.width = '80%'
    return yr


def color_palette_picker():
    '''
    Return a string of color indicator from users' manual pick
    '''
    return Dropdown(options={'Ocean': 'PuBu',
                             'Orchid': 'RdPu',
                             'NYU Pride': 'BuPu',
                             'Alert': 'OrRd',
                             'Water Green': 'GnBu',
                             'Autumn Leaf': 'YlOrBr'
                             },
                    value='PuBu',
                    description='Palette',
                    disabled=False,
                    button_style='info'
                    )


def Display_Your_Choropleth():
    '''
    Allow users to interactively explore data information
    and customize the choropleth map
    '''
    try:
        interact(plot_choropleth,
                 Year=year_slider(),
                 Feature=ht.feature3_picker(),
                 Color=color_palette_picker()
                 )
    except NoDataError as x:
        print(x)
