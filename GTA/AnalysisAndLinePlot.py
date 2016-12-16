'''
This module allows users to:
    - select country or the whole world
    - get the overall statistical analyzing information of chosen country
    - visualize the terrorism caused occurrences, casualties, deaths or wounds
    - make 'smooth line' visualization
    - select feature
    - customize color

Module Author: Xianzhi Cao (xc965)
Project co-author: Caroline Roper (cer446)
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import data
from scipy.interpolate import spline
from ipywidgets import interact, ColorPicker, Dropdown
from UserError import NoCountryDataError


def set_as_index(df, colname):
    '''
    Parameter
        - df                                                | DataFrame
        - colname: feature name, e.g. 'year' and 'country'  | str
    Return
        a DataFrame with colname as index
    '''
    return df.set_index(colname)


def df_occur_by_ctr(ctr_name):
    '''
    Parameter
         - ctr_name: country name or "The Whole World"      | str
    Return
         - number of attacks in the chosen country
           across the whole time series
           (non-attack years not included)                  | DataFrame
    '''
    df = data.load_df()
    if ctr_name == 'The Whole World':
        df_all_c = df
    # It is necessary to convert the variable "df_call_c"
    # to the transposing DataFrame format,
    # for countries with only one time attack occurrence.
    # Otherwise will cause bugs
    else:
        df_all_c = set_as_index(df, 'country').ix[ctr_name]
        if type(df_all_c) == pd.Series:  # for those countries with only one attack
            df_all_c = pd.DataFrame(df_all_c).T
    df_yr = pd.DataFrame(df_all_c.groupby('year').count().eventid)
    # rename the 'count' column as 'occurrences' to avoid unexpected potential misusage
    df_yr.columns = ['occurrences']
    return df_yr.reset_index()


def df_occur_by_ctr_allyears(ctr_name):
    '''
    Parameter
         - ctr_name: country name                               | str
    Return
         - number of attack occurrences
           in the chosen country
           across the whole time series
           (all years included, including non-attack years)     | DataFrame
    '''
    dic_yr = {'year': list(range(1970, 2016)),
              'null': np.zeros((2015-1970)+1, dtype=int)}
    df_years = pd.DataFrame(dic_yr)
    df_full_yr = pd.merge(df_years, df_occur_by_ctr(ctr_name),
                          on='year', how='outer').fillna(0)  # merge all years
    return df_full_yr[['year', 'occurrences']]


def gtd_country_names():
    '''
    Return a list of:
        - all country names in alphabetical order, plus
        - 'The Whole World'
    '''
    all_ctr = sorted(data.load_df().country.unique())
    all_ctr.insert(0, 'The Whole World')
    return all_ctr


def drop93(df):
    '''
    Parameter
        - df: a Dataframe with feature "year"     | DataFrame
    Return
        a DataFrame without the year 1993,
        since there is no data in the GT Database
    '''
    return df[df.year != 1993]


def df_ctr(Country):
    '''
    Parameter
        - Country: name of a country or "The Whole World"   | str
    Return
        a DataFrame with selected features
    '''
    if Country == 'The Whole World':
        df_ctr = data.load_df()
    else:
        df_ctr = data.load_df()[data.load_df().country == Country]
    return df_ctr.drop(['eventid', 'latitude', 'longitude'], 1)


def df_ctr_all(Country):
    '''
    Parameter
        Country: name of a country or "The Whole World"   | str
    Return
        a DataFrame (excluding 1993)
    Features
        - year: 1970 to 2015
        - number of kills, wounds and casualties
        - number of annual attack occurrences
    '''
    df1 = df_ctr(Country).groupby('year').sum().reset_index()
    df2 = df_occur_by_ctr_allyears(Country)
    df_merge = pd.merge(df1, df2, on='year', how='outer').fillna(0).sort_values(by='year')
    df = df_merge.reset_index().drop(['index'], 1)
    return drop93(df)  # drop the data-lacking year in the original dataset


def ctr_stats(Country):
    '''
    Return a statistical analyzing table of
    the chosen country's attack data
    across the whole time series                 | DataFrame
    '''
    ctr_stats = df_ctr_all(Country).describe().T
    ctr_stats['sum'] = df_ctr_all(Country).sum()
    return ctr_stats

def analy_ctr(Country):
    '''
    Return a structured statistical analysis
    of the chosen country's attack data
    across the whole time series                 | String
    '''
    desc = ctr_stats(Country)
    df_ixby_yr = df_ctr_all(Country).set_index('year')
    analysis_str = '\
                      Statistical Analysis - Terrorism Attacks in {}                        \n\
                                                * * *                                       \n\
--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--\n\
                During the year 1970 to 2015:                                               \n\
                - The year with the most attacks:        {}                                 \n\
                         * {} times of terror attacks in {} in this year                    \n\
                - The year with the most casulties:      {}                                 \n\
                         * {} suffered the most severe damage by terrorism in this year.    \n\
                         * {} people were killed or wounded.                                \n\
                         * {} times of terror attacks in {} in this year                    \n\
                - Occurrences of Terrorism Attacks                                          \n\
                         * The total number:              {} \n \
                        * The annual average:            {} \n \
                        * The standard deviation:        {} \n \
               - Casualties                                 \n \
                    1) The total number:                 {} \n \
                        * kills                          {} \n \
                        * wounds                         {} \n \
                    2) The annual average:               {} \n \
                        * kills                          {} \n \
                        * wounds                         {} \n \
                    3) The standard deviation:           {} \n \
                        * kills                          {} \n \
                        * wounds                         {} \n \
--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--\n'
    analysis = analysis_str.format(Country,
                                   np.argmax(df_ixby_yr.occurrences),               # the year with maximum occurrence
                                   int(df_ixby_yr.occurrences.max()),               # the maximum occurrence
                                   Country,
                                   np.argmax(df_ixby_yr.casualties),          # the year with maximum casualties
                                   Country,
                                   str(int(desc.loc['casualties', 'max'])),   # the largest number of casualties
                                   str(int(desc.loc['occurrences', 'max'])),        # the largest number of occurrences
                                   Country,
                                   str(int(desc.loc['occurrences', 'sum'])),        # total number of attacks
                                   str(int(desc.loc['occurrences', 'mean'])),       # mean of annual attacks
                                   str(desc.loc['occurrences', 'std']),             # std of annual attacks
                                   str(int(desc.loc['casualties', 'sum'])),   # total number of casualties
                                   str(int(desc.loc['kills', 'sum'])),        # total number of people killed
                                   str(int(desc.loc['wounds', 'sum'])),       # total number of wounded
                                   str(int(desc.loc['casualties', 'mean'])),  # mean of annual casualties
                                   str(int(desc.loc['kills', 'mean'])),       # mean of annual kills
                                   str(int(desc.loc['wounds', 'mean'])),      # mean of annual wounds
                                   str(desc.loc['casualties', 'std']),        # std of annual casualties
                                   str(desc.loc['kills', 'std']),             # std of annual kills
                                   str(desc.loc['wounds', 'std']),            # std of annual wounds
                                  )
    return analysis

def analy_and_plot(Country, Feature, Color):
    '''
    Parameters
        - Country: country name          | str
        - Feature: type of damage        | str
        - Color:   color of plot         | str
    Return
        - Line Plot in smoothed fashion  | Plot
        - Statistical analysis           | String
    '''
    # Country input should be from the GTD database country names
    if Country not in gtd_country_names():
        raise NoCountryDataError

    else:
        fig = plt.figure(figsize=(15, 5))

        df = df_ctr_all(Country)
        x = df.year
        y = df[Feature]
        mean = ctr_stats(Country)['mean'].loc[Feature]

        # set smooth linestyle
        x = np.array(x)
        y = np.array(y)
        x_smooth = np.linspace(x.min(), x.max(), 500)
        y_smooth = spline(x, y, x_smooth)  # use spline in scipy library to smooth

        # set the seaborn gird background as white
        sns.set(style="whitegrid")
        plt.plot(x_smooth, y_smooth, '-', color=Color, linewidth=3,
                 label='{} in {}'.format(Feature.capitalize(), Country))
        plt.axhline(y=mean, label='Average {}'.format(Feature.capitalize()),
                    color='k', linewidth=1, linestyle='dashed')
        plt.ylim(ymin=0)
        plt.title('Terror Attack {} in {} (1970-2015)'.format(Feature.capitalize(), Country), size=16)
        plt.xlabel('Year', size=14)
        plt.ylabel('Number of Terror {}'.format(Feature.capitalize()), size=14)
        plt.legend()
        plt.show()
        print(analy_ctr(Country))


def color_picker():
    '''
    Return a tring of color from users' manual pick
    '''
    clr = ColorPicker(concise=False,
                      description='Color:',
                      value='#5BC0DE'
                      )
    return clr


def country_picker():
    '''
    Return a string of country name from users' manual pick
    '''
    return Dropdown(options=gtd_country_names(),
                    value='The Whole World',
                    description='Country:',
                    disabled=False,
                    button_style='info'
                    )


def feature4_picker():
    '''
    Return a string of feature name from users' manual pick
    '''
    return Dropdown(options={'Occurrence': 'occurrences',
                             'Casualty': 'casualties',
                             'Death': 'kills',
                             'Wound': 'wounds'},
                    value='occurrences',
                    description='Feature:',
                    disabled=False,
                    button_style='info'
                    )


def Display_Your_Analysis_And_LinePlot():
    '''
    Allow users to interactively explore data information
    and customize:
        - the lineplot
        - the Statistical Analysis
    '''
    try:
        interact(analy_and_plot,
                 Country=country_picker(),
                 Feature=feature4_picker(),
                 Color=color_picker())
    except NoCountryDataError as x:
        print(x)
