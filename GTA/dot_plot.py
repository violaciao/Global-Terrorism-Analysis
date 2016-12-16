'''
This module:
1) Processes data within the Dot_Plot_Data class. This class is intended to be somewhat flexible so that programmers
can consider alternate reconfigurations of the dot plot or use different data in the future.
2) Defines a function that prepares a dot plot and then plots it.
3) Defines widgets that the user can manipulate so that they can alter the appearance of the dot plot.
4) Defines a function that applies the input captured by the widgets to the dot plot.

Module Author: Caroline Roper (cer446)
Project co-author: Viola Ciao (xc965)
'''


from __future__ import print_function
from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets

import pandas as pd
import seaborn as sns
import math

from util import *
from Geo2D import year_interval_slider
import heatmap as ht

global_terrorism = ht.GTA()
global_terrorism.gt_df.head()

dot_plot_features = ['country', 'year', 'attacktype', 'casualties']
gtd_dot = global_terrorism.gt_df[dot_plot_features]


class Dot_Plot_Data():
    def __init__(self, data, yaxis_vals, xaxis_vals, user_filter1, user_filter2, metric):
        '''Defines attributes of the dot plot'''
        self.data = data[[yaxis_vals, xaxis_vals, user_filter1, user_filter2]]
        self.yaxis_vals = yaxis_vals
        self.xaxis_vals = xaxis_vals
        self.user_filter1 = user_filter1
        self.user_filter2 = user_filter2
        self.subgroups = group_by_columns(self.data, [self.yaxis_vals, self.user_filter1, self.user_filter2], self.xaxis_vals)
        self.metric = metric
        if self.metric == 'occurrences':
            self.count_by_subgroup()
        if self.metric == 'casualties':
            self.sum_by_subgroup()

    def count_by_subgroup(self):
        '''Uses group from init function to create a count'''
        self.data = unstack_table(count_by_groups(self.subgroups))

    def sum_by_subgroup(self):
        '''Uses sum from init function to create a sum'''
        self.data = unstack_table(sum_by_groups(self.subgroups))

    def user_selection(self, year_tuple, attack_type):
        '''Selects year and attack type'''
        years = tuple(range(year_tuple[0], year_tuple[1]+1))
        self.attack_type = attack_type
        self.data = self.data.loc[:, (slice(None), attack_type, years)]

    def aggregate(self):
        '''sum horizontally'''
        self.data = self.data.sum(axis=1)

    def convert_series(self, label):
        '''Takes a series and label for the series' values, returns dataframe with 2 columns: the series' row index, & the series' values'''
        self.label = label
        self.data = pd.DataFrame(self.data)
        self.data.columns = [label]
        self.data.reset_index(level=0, inplace=True)

    def take_top_20(self):
        '''Sorts and takes top 20 values'''
        self.data = self.data.sort_values(self.label, ascending=False).iloc[0:20, :]


def create_dot_plot(metric, attacktype, year_range):
    '''Creates a dot plot with input specifications'''
    #Portions of this code were adapted from: http://seaborn.pydata.org/examples/pairgrid_dotplot.html

    pd.options.mode.chained_assignment = None

    dot_plot = Dot_Plot_Data(global_terrorism.gt_df, 'country', 'casualties', 'year', 'attacktype', metric)

    dot_plot.user_selection(year_range, attacktype)
    dot_plot.aggregate()
    dot_plot.convert_series(str.title(metric) + ' from ' + attacktype)
    dot_plot.take_top_20()

    sns.set(style="whitegrid")

    g = sns.PairGrid(dot_plot.data,
                     x_vars=str.title(metric) + ' from ' + attacktype, y_vars=['country'],
                     size=12, aspect=.50)

    # Draw a dot plot using the stripplot function
    g.map(sns.stripplot, size=10, orient="h",
          palette="Blues_r", edgecolor="gray")

    xmax = math.ceil(max(dot_plot.data[dot_plot.label])/1000)*1000

    g.set(xlim=(0, xmax), xlabel=str.title(metric), ylabel=str.title(dot_plot.yaxis_vals))

    # Use meaningful titles for the columns
    titles = ['Top Countries by ' + attacktype + ' ' + str.title(metric)]

    for ax, title in zip(g.axes.flat, titles):

        # Set a different title for each axes
        ax.set(title=title)

        # Make the grid horizontal instead of vertical
        ax.xaxis.grid(False)
        ax.yaxis.grid(True)

    sns.despine(left=True, bottom=True)

def attack_type():
    '''Return a string corresponding to an attack type'''
    attacktypes = list(set(global_terrorism.gt_df['attacktype']))
    attack_type = widgets.Dropdown(
                                options=attacktypes,
                                value='Armed Assault',
                                description='Attack Type:',
                                disabled=False,
                                button_style='info') # 'success', 'info', 'warning', 'danger' or ''
    return attack_type

def metric_selection():
    '''
    Return a string of util name from users' manual pick
    '''
    metric = widgets.ToggleButtons(options={'Occurrences': 'occurrences', 'Casualties': 'casualties'},
                         value='occurrences',
                         description='Metric:',
                         disabled=False,
                         button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                         tooltip='Description')
    return metric

def Display_Your_Dot_Plot():
    '''
    Allow users to customize the dot plot
    '''
    interact(create_dot_plot, metric = metric_selection(), attacktype = attack_type(), year_range = year_interval_slider());
