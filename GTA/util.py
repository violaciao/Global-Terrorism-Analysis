'''
This modules contains various functions common to all the data visualizations.
Functions includes:
    - feature selection
    - feature renaming
    - extract unique names
    - convert feature value series into list
    - group columns and other uses

Module Authors: Xianzhi Cao (xc965) and Caroline Roper (cer446)
'''


import numpy as np
import pandas as pd
import data


def selection():
    '''
    feature selection
    '''
    features = ['eventid', 'iyear', 'country_txt', 'region_txt', \
                'latitude', 'longitude', \
                'attacktype1_txt', 'nkill', 'nwound']
    return features


def feature_names():
    '''
    rename the features for easier re-processing
    '''
    return ['year', 'country', 'region', 'latitude', 'longitude', \
                         'attacktype', 'kills', 'wounds']


def make_array(dataset, col_name):
    '''
    Parameter
        - dataset                                         | DataFrame
        - col_name                                        | str
    Return
        an array of all lists of selected feature values  | np.array
    '''
    new_list = []
    for i in dataset[col_name].values.tolist():
        new_list.append(i)
    return np.array(new_list)


def make_log_array(dataset, col_name):
    '''
    Parameter
        - dataset                                 | DataFrame
        - col_name                                | str
    Return
        values of selected feature (in logarithm) | np.array
    '''
    new_list = []
    for i in dataset[col_name].values.tolist():
        new_list.append(np.log(i))
    return np.array(new_list)


def df_sel_btw_years(year_interval):
    '''
    Parameter
        - year_interval: Time Interval           |   tuple
    Return
        - all data in the chosen time interval   |   DataFrame
    '''
    gt_df = data.load_df()
    df_intv = gt_df[(gt_df.year <= year_interval[1]) & (gt_df.year >= year_interval[0])]
    return df_intv


def make_five_year_start(dataset):
    '''
    Parameter
        - dataset | DataFrame
    Return a new DataFrame with a new feature 'period'
        periods are partitioned by every 5 years
        eg. period 1990 means from year 1990 to year 1994
    '''
    dataset['period'] = [int(i/5)*5 for i in dataset.year]
    return dataset


def unstack_table(data):
    '''Unstacks data until there's only one row index remaining'''
    data = data.fillna(0)
    i = 0
    while i < data.index.nlevels:
        data = data.unstack()
        i = i + 1
    return data

def convert_series(series, label):
    '''Takes a series and label for the series' values, returns df with 2 columns: the series' row index, & the series' values'''
    converted = pd.DataFrame(series)
    converted.columns = [label]
    converted.reset_index(level=0, inplace=True)
    return converted

def group_by_columns(data, group_by_columns, column_to_agg):
    '''Takes a list of column names and a column to count and counts rows by those column name, including nulls'''
    all_columns = group_by_columns + [column_to_agg]
    data.loc[:, column_to_agg] = data.loc[:, column_to_agg].fillna(value=0)
    data = data.loc[:,all_columns]
    grouped = data.groupby(group_by_columns)
    return grouped

def sum_by_groups(grouped):
    '''Takes output of group function and sums data'''
    sums = grouped.sum().dropna()
    sums.columns = ['sum']
    return sums

def count_by_groups(grouped):
    '''Takes output of group function and counts data'''
    counts = grouped.count().dropna()
    counts.columns = ['count']
    return counts

def create_range(series_to_group, group_size):
    '''Turns a series into groups of a specified size'''
    bins = np.arange(min(series_to_group) - group_size, max(series_to_group) + group_size, group_size)
    ranges = pd.cut(series_to_group, bins)
    ranges.name = series_to_group.name + ' ranges'
    return ranges

def replace_series_with_range(data, series_to_group, group_size):
    '''Removes year column and merges range column'''
    ranges = create_range(series_to_group, group_size)
    data_replaced = pd.concat([data, pd.DataFrame(ranges)], axis = 1).drop(series_to_group.name, 1)
    return data_replaced
