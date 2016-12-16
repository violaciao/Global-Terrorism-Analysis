'''
This module contains
    - functions to plot 2D geo map with Basemap
    - functions to assist the plot

This module allows users to
    - select year interval with ipywidgets
    - visualize the terror attacks' occurrence density
    - customize map background

@author: Xianzhi Cao (xc965)
'''


# Exception handling if not successfully loading Basemap
try:
    from mpl_toolkits.basemap import Basemap
except ImportError:
    print('Basemap is not installed. The density plot will not render until you have installed it.\n\
        Please visit the User Guide for instructions on how to install it. Thank you.')


import matplotlib.pyplot as plt
import pandas as pd
import util as ut
import data
import re
from ipywidgets import *
from UserError import *


def plot_2D_density(Year, MapStyle):
    '''
    Parameters
        - Year      : between 1970-2015     | str
        - MapStyle  : style palette         | str
    Return
        A 2D Geo Map: The denser the red marker in a country,
                      the more severe damages had taken place.
    '''
    # use regular expression to check the format
    if not re.match(r'[\[|\(][0-9]{4}\,\s?[0-9]{4}[\]|\)]$', str(Year)):
        raise NotIntervalError

    # the starting year should be less than the ending yer
    elif Year[0] >= Year[1]:
        raise IntervalReverseError

    # catch the missing value exceptions in 1993
    elif Year == (1993, 1993):
        print('Data of 1993 is not available in Global Terrorism Database.\n\
Click the link to learn why.\nhttps://www.start.umd.edu/gtd/faq/')

    # catch the out of range yer interval input errors
    elif (Year[0] < 1970) or (Year[1] > 2015):
        raise IntervalLeakError

    else:
        if Year[0] == Year[1]:  # catch the excetion the starting year and the ending year converge
            df_gt = data.load_df()
            df = df_gt[df_gt.year == Year[0]]
        else:
            df = ut.df_sel_btw_years(Year)

        plt.figure(figsize=(18,10), frameon=False)

        m = Basemap('mill')
        m.drawcountries(linewidth=0.5,
                        linestyle='solid',
                        color='white',
                        antialiased=1,
                        ax=None,
                        zorder=None
                        )

        # Background settings
        if MapStyle == 'Blue Marble':
            m.drawcoastlines()
            m.bluemarble()
        elif MapStyle == 'Etopo':
            m.etopo()
        else:
            m.drawcoastlines(color='w')
            m.drawcountries(color='w')
            m.drawstates(color='w')
            m.fillcontinents(color='lightblue',lake_color='w')
            m.drawmapboundary(fill_color='w', color='w')

        # get latitude and longitude
        lat = ut.make_array(df, 'latitude')
        lon = ut.make_array(df, 'longitude')

        x,y = m(lon, lat)
        m.plot(x, y, 'r^', marker='o', markersize=4, alpha=.3)

        plt.title('Global Attack Density Plot: {}-{}'.format(Year[0], Year[1]), size=16)
        plt.show()


def year_interval_slider():
    '''
    Return a year interval from ipywidgets' IntSlider by users' manual pick
    '''
    yr_interval = IntRangeSlider(value=[1996, 2000],
                                 min=1970,
                                 max=2015,
                                 step=1,
                                 description='Year:',
                                 disabled=False,
                                 continuous_update=False,
                                 orientation='horizontal',
                                 readout=True,
                                 readout_format='i',
                                 slider_color='white',
                                 color='black')
    yr_interval.layout.width = '80%'
    return yr_interval


def map_style_picker():
    '''
    Return a string from ipywidgets' Dropdown box by users' manual pick
    '''
    return Dropdown(options=('Blue Marble', 'Etopo', 'Plain'),
                    value='Plain',
                    description='Map Style:',
                    disabled=False,
                    button_style='info')


def Display_Your_Geo2D_Map():
    '''
    Allow users to interactively explore data information
    and customize the 2D Geo Map
    '''
    interact(plot_2D_density, Year=year_interval_slider(), MapStyle=map_style_picker())
