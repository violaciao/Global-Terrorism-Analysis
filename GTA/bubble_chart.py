'''
This module:

1) Prepares a dataset to be turned into a bubble chart: selects features, creates ranges from numeric features
2) Aggregates and reshapes the data within the Bubble_Chart_Data class. This class is intended to be flexible so that
programmers can easily adapt it to reconfigure new bubble charts or use these techniques on different data.
3) Plot the bubble chart with appropriate legends, titles, and formatting.
4) Creates a function that allows users to scroll through the bubble chart over time.


module author: Caroline Roper
project co-author: Viola Ciao
'''

from ipywidgets import *
import pandas as pd
import numpy as np
import heatmap as ht
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mpatches
import util
from matplotlib import cm

Global_terrorism_analysis = ht.GTA()
bubble_chart_features = ['year', 'country', 'region', 'casualties']
gtd_bubble = Global_terrorism_analysis.gt_df[bubble_chart_features]
gtd_bubble = util.replace_series_with_range(gtd_bubble, gtd_bubble['year'], 5)

def construct_interval(year):
    '''Constructs an interval given a year'''
    return '('+ str(year - 5) + ', ' + str(year) + ']'

def draw_legend(colors_legend):
    '''Draws a legend according to a dictionary'''
    recs = []
    for key in list(colors_legend.keys()):
        recs.append(mpatches.Rectangle((0,0),1,1,fc=colors_legend[key], alpha = 0.5))
    plt.legend(recs,list(colors_legend.keys()),loc=4)

class Bubble_Chart_Data():
    def __init__(self, data, bubble_id, color, user_filter, values):
        '''Defines attributes of the bubble chart'''
        self.data = data
        self.bubble_id = bubble_id
        self.color = color
        self.user_filter = user_filter
        self.values = values
        self.new_data = data
        self.groups = util.group_by_columns(self.data, [self.bubble_id], self.values)
        self.subgroups = util.group_by_columns(self.data, [self.bubble_id, self.color, self.user_filter], self.values)
        self.x_values = values
        self.y_values = values

    def count_by_subgroup(self):
        '''Uses group from init function to create a count'''
        return util.count_by_groups(self.subgroups)

    def sum_by_subgroup(self):
        '''Uses sum from init function to create a sum'''
        return util.sum_by_groups(self.subgroups)

    def aggregate_by_subgroup(self):
        '''Returns sum and count merged together'''
        self.new_data = pd.concat((self.count_by_subgroup(), self.sum_by_subgroup()), axis=1, join='outer')
        self.new_data.columns = ['occurrences', self.values]
        self.new_data.reset_index(level=self.color, inplace=True)

    def count_by_group(self):
        '''Returns the sum by groups (ignores user filters)'''
        return util.count_by_groups(self.groups)

    def set_bubble_size(self, bubble_size, new_col_name):
        '''bubble size must be a one-column dataframe or series with the bubble_id as the index'''
        self.new_data = pd.DataFrame(bubble_size).join(self.new_data, how='inner')
        self.new_data = self.new_data.rename(index=str, columns={pd.DataFrame(bubble_size).columns[0]: new_col_name})
        self.bubble_size = new_col_name

    def set_x_axis_values(self, x_values):
        '''Stores the column name corresponding to the bubbles' values on the x-axis'''
        self.x_values = x_values

    def set_y_axis_values(self, y_values):
        '''Stores the column name corresponding to the bubbles' values on the y-axis'''
        self.y_values = y_values

    def add_color_dict(self):
        '''Creates a dictionary that maps the color variable to numbers, should be called after aggregate'''
        #Used this resource: http://stackoverflow.com/questions/14885895/color-by-column-values-in-matplotlib
        color_cats = self.data[self.color].unique()
        colors = np.linspace(0, 1, len(color_cats))
        colordict = dict(zip(color_cats, colors))
        self.new_data['color'] = self.new_data[self.color].apply(lambda x: colordict[x])

    def process_bubble_chart_data(self, x_values, y_values):
        '''Prepares bubble chart to be plotted'''
        self.aggregate_by_subgroup()
        self.set_bubble_size(self.count_by_group(), 'all-time occurrences')
        self.set_x_axis_values(x_values)
        self.set_y_axis_values(y_values)
        self.add_color_dict()
        self.new_data.reset_index(level=self.bubble_id, inplace=True)

    def filter_for_user(self, user_input):
        '''Selects the part of the data that the user selected, should be called after aggregate'''
        self.new_data = self.new_data.loc[user_input, :]

    def create_legend(self):
        '''Takes an object from the bubble chart data class and creates an appropriate legend. Must be called after process data'''
        grouped_by_color = util.group_by_columns(self.new_data, [self.color, 'color'], self.bubble_id)
        counted_by_color = util.count_by_groups(grouped_by_color)
        counted_by_color.reset_index(inplace=True)

        colors_legend = {}

        for i in range(0, len(counted_by_color)):
            colors_legend[counted_by_color[self.color][i]] = cm.viridis(counted_by_color['color'][i])

        return colors_legend

    def annotate(self):
        '''Labels the top 10 bubbles by the attribute that will be on the y-axis'''
        self.new_data.sort_values(self.y_values, ascending=False).iloc[0:20]
        for i in range(0, 10):

            offset_x = math.sqrt(self.new_data[self.bubble_size].iloc[i])/4
            offset_y = - math.sqrt(self.new_data[self.bubble_size].iloc[i])/25

            plt.annotate(self.new_data[self.bubble_id].iloc[i],
                         xy = (self.new_data[self.x_values].iloc[i], self.new_data[self.y_values].iloc[i]),
                         xytext=(offset_x, offset_y),
                         textcoords='offset points',
                         color='darkslategrey')

    def format_axes_length(self, ax):
        '''Formats axes lengths according to range of values to present'''
        x_limit = math.ceil(max(self.new_data[self.x_values])/750)*750
        y_limit = math.ceil(max(self.new_data[self.y_values])/7500)*7500
        ax.set_xlim(xmin = -0.05*x_limit, xmax = x_limit )
        ax.set_ylim(ymin = -0.05*y_limit, ymax = y_limit )

    def format_labels(self, ax):
        '''Creates meaningful chart title and axis labels'''
        ax.set_title(str.title(self.x_values) + ' and ' + str.title(self.y_values) + ' by ' + str.title(self.bubble_id))
        ax.title.set_fontsize(15)
        ax.set_xlabel(str.title(self.x_values))
        ax.set_ylabel(str.title(self.y_values))

    def create_bubble_chart(self, year):
        '''Draws the bubble chart'''
        self.process_bubble_chart_data('occurrences', 'casualties')
        self.filter_for_user(construct_interval(year))
        self.new_data = self.new_data.sort_values(self.values, ascending=False)

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, axisbg='white')

        self.format_labels(ax)

        ax.scatter(self.new_data[self.x_values],
                         self.new_data[self.y_values],
                         self.new_data[self.bubble_size]/5,
                         c = self.new_data['color'],
                         cmap = 'viridis',
                         alpha = 0.5)

        self.new_data.sort_values(self.y_values, ascending=False).iloc[0:20]
        self.annotate()

        draw_legend(self.create_legend())

        self.format_axes_length(ax)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)

        plt.show()

bubble_chart = Bubble_Chart_Data(gtd_bubble, 'country', 'region', 'year ranges', 'casualties')

def Display_Your_Bubble_Chart():
    '''
    Allow users to interactively explore data information
    and customize the bubble chart
    '''
    interact(bubble_chart.create_bubble_chart, year=IntSlider(min=1975,max=2015,step=5,value=1995, width = '90%', description =  'End 5yr Range'))