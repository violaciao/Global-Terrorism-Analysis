'''
This module:
    - converts the excel dataset file into the csv file
    - processes the dataset with selected features
    - get new dataframe
    - store the new dataframe in csv file
    - load country geo json file into dict

The whole process simply aims at generating the original dataset
and shortening the loading time for future data manipulations.

@author: Xianzhi Cao (xc965)
'''

import pandas as pd
import re
import json
import util as ut
from UserError import *


# Data Preparation Function
def excel_to_csv(path_excelfile):
    '''
    Notice! We used this function to convert the original dataset into csv file
    Due to the massive dataset volumn with long converting time,
    we have uploaded the a ready-to-use 'gtd_wholedata.csv' file online.

    Instructions for how to download this dataset is in the User Manual.
    Please make sure that you have the required dataset downloaded to your local repository.

    ---

    Input:  load the original database          | excel
    Output: save it the excel file into csv     | csv
    '''
    path = 'globalterrorismdb_0616dist.xlsx'
    if path_excelfile == path:
        whole = pd.read_excel(path_excelfile)
        whole.to_csv('gtd_wholedata.csv')
    else:
        raise WrongDatafileError


# Data Preparation Function
def load_raw():
    '''
    read csv file created by excel_to_csv function
    '''
    df_raw = pd.read_csv('gtd_wholedata.csv', usecols=ut.selection(),
                         low_memory=False, index_col=0).fillna(0)
    return df_raw


# Data Preparation Function
def make_df():
    '''
    make the DataFrame with selected features
    rename the features
    add "casualties" as sum of "kills" and "wounds"
    ***
    converted all the number of kills, wounds and casualties to integer
    in case of unexpected bugs
    '''
    df = load_raw()
    df.columns = ut.feature_names()
    df[['kills', 'wounds']] = df[['kills', 'wounds']].astype(int)
    df['casualties'] = df.kills + df.wounds
    return df


# Data Preparation Functions
def save_df_csv():
    '''
    make a csv file with all selected features
    '''
    return make_df().to_csv('gtd_wholedata_selected.csv')


### Above are functions serve for data preparations
### for a better user experience
### we have pre-processed the dataset
### and made our project ready to use


def load_df():
    '''
    The MOST BASICALLY USED loading function in this program,
    load the DataFrame with selected features
    '''
    df = pd.read_csv('gtd_wholedata_selected.csv')
    return df

def df_year_idx():
    '''
    return the DataFrame with selected features, indexed by years
    '''
    return pd.read_csv('gtd_wholedata_selected.csv', index_col='year')


def load_json_file(filepath):
    '''
    Input:  Json file with country coordinates     | json
    OUtput: all the countries with their geo info  | dict
    ---
    NB: Using the with open method in json library
    returns a stabler output than using pandas' read json
    according to my practical experiement.
    '''
    # use regular expressions to check whether the input is a json file
    if not re.match(r'.+\.(json){1}$', filepath):
        raise LoadJsonError  # Error when not taking a json file as input
    else:
        with open('countries.geo.json') as json_data:
            j = json.load(json_data)
    return j
