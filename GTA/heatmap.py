'''
This module includes:
    - GTA class, with the attrubutes:
        1. feature-selected dataframe of Global Terrorism Database
        2. a unieque list of region names
    - visualization function of the dataset in heatmap
    - the target feature
    - the visualizing color palette

@author: Xianzhi Cao (xc965)
'''


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from util import *
from data import *
from ipywidgets import interact, ToggleButtons, Dropdown


class GTA(object):
    '''
    contains attributes of:
        - DataFrame of Global Terrorism data selection
        - list of all regions' names
        - function of get
    '''
    def __init__(self):
        self.gt_df = load_df()
        self.region_names = self.gt_df.region.unique().tolist()


    def countries_by_region(self):
        '''
        Return a dict with items:
            - keys:    region names
            - values:  country names keyed by certain region
        '''
        country_names = {}
        for region in self.region_names:
            country_names[region] = self.gt_df[self.gt_df.region == region].dropna().country.unique()
        return country_names


def Heatmap_by_region(Feature, Region, Cmap):
    '''
    Parameters
        - Feature: feature of damages       | str
        - Region : name of region           | str
        - Cmap   : color map                | str
    Return
        A Heatmap
            of a comparison of values by chosen Feature
            among countrys in chosen region, colored with chosen cmap
    '''
    dat = GTA().gt_df[GTA().gt_df.region == Region]  # DataFrame filtered with region
    couple_cols = dat[['year', 'country', Feature]]
    couple_cols.reset_index(inplace=True)
    cp_cols = couple_cols.drop('index', 1)
    y_c = cp_cols.groupby(['year', 'country']).sum()
    y_c = y_c.reset_index()

    # proportionally set the height of the figure size
    # by the number of countries in the chosen region
    fig = plt.figure(figsize=(25, int(len(GTA().countries_by_region()[Region])*3/4)))

    # use pivot table to set data in heatmap plot format
    pivot_table = y_c.pivot('country', 'year', Feature).fillna(0)
    plt.title('Yearly Number of {} in {} by Terror Attacks (1970-2015)\n'.format(Feature.capitalize(),
                                                                               Region), size = 20)
    plt.xlabel('Regions', size = 14)
    plt.ylabel('Years', size = 14)
    plt.xticks(rotation=-15)

    # use pivot table to plot heatmap
    sns.heatmap(pivot_table,
                annot=False,
                fmt='.0f',
                linewidths=.5,
                square=True,
                cmap=Cmap,
                cbar_kws={"orientation": "horizontal"}
                )
    plt.show()


def region_picker():
    '''
    Return a string of region name from users' manual pick
    '''
    return Dropdown(options=GTA().region_names,
                    value='Southeast Asia',
                    description='Region',
                    disabled=False,
                    button_style='info' # 'success', 'info', 'warning', 'danger' or ''
                    )


def Cmap_palette_picker():
    '''
    Return a string of color from users' manual pick
    '''
    return Dropdown(options={'Aqua': 'cool',
                             'Lemon': 'Wistia',
                             'NYU Pride': 'Purples',
                             'Classic': 'RdBu_r'
                             },
                    value='RdBu_r',
                    description='Palette',
                    disabled=False,
                    button_style='info')



def feature3_picker():
    '''
    Return a string of feature name from users' manual pick
    '''
    return ToggleButtons(options={'Deaths': 'kills',
                                  'Wounds': 'wounds',
                                  'Casualties': 'casualties'
                                  },
                         value='casualties',
                         description='Feature',
                         disabled=False,
                         button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                         tooltip='Description')


def Display_Your_Heatmap():
    '''
    Allow users to interactively explore data information
    and customize the heatmap
    '''
    interact(Heatmap_by_region,
             Region=region_picker(),
             Cmap = Cmap_palette_picker(),
             Feature = feature3_picker())
