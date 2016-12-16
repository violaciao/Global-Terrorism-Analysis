'''
This module tests:
    - all visualization classes and its methods
    - all the crucial functions in this program
    - exceptions and errors

@author: Xianzhi Cao (xc965)
'''

import unittest
import pandas as pd
import numpy as np
import util as ut
import AnalysisAndLinePlot as al
import choropleth as cr
import heatmap as ht
import Geo2D as geo
from data import *
from UserError import *


class UserTest(unittest.TestCase):
    """
    This class allows users to run tests with classes and functions.
    """

    def setUp(self):
        pass


    def test_make_df(self):
        '''
        test the make_df function in the data module
        whether returns the correct DataFrames
        '''
        # test if the appended feature name 'casualties' is in the column names
        self.assertTrue('casualties' in make_df().columns.tolist())
        # test whether the length of DataFrame is greater than 150,000
        self.assertGreater(make_df().shape[0], 150000)


    def test_load_json_file(self):
        '''
        test the load_json_file function in the data module
        whether the expected exceptions and errors occurred
        when non-json file is uploaded
        '''
        test_path = 'gtd_wholedata.csv'
        # test when year input is emtpy
        with self.assertRaises(LoadJsonError):
            load_json_file(filepath=test_path)


    def test_make_array(self):
        '''
        test the make_array function in the util module
        whether the correct income lists are returned
        '''
        df_test1 = pd.read_csv('https://bit.ly/uforeports')
        self.assertEqual(np.ndarray, type(ut.make_array(df_test1, 'City')))


    def test_df_sel_btw_years(self):
        '''
        test the df_sel_btw_years function in util module
        whether the output DataFrame is in the expected time range
        '''
        self.assertTrue(2002 in list(ut.df_sel_btw_years((2000, 2005)).year))
        self.assertFalse(1990 in list(ut.df_sel_btw_years((2000, 2005)).year))


    def test_make_five_year_start(self):
        '''
        test the make_five_year_start function in the util module
        whether the values in the new feature 'period'
        can be devided by 5.
        '''
        df3 = ut.make_five_year_start(load_df())
        self.assertTrue('period' in df3)
        self.assertTrue(2000 in list(df3[df3.year.isin([2001, 2002, 2004])].period))
        self.assertNotIn(2005, list(df3[df3.year.isin([2001, 2002, 2004])].period.values))

    #################

    # Caroline's test goes here

    #################


    def test_df_occur_by_ctr(self):
        '''
        test the df_occur_by_ctr function in AnalysisAndLinePlot module
        whether the return DataFrame is in expected format with correct values
        '''
        self.assertEqual(['year', 'occurrences'], list(al.df_occur_by_ctr('Germany').columns))
        self.assertEqual(['year', 'occurrences'], list(al.df_occur_by_ctr('The Whole World').columns))
        self.assertEqual(pd.Index, type(al.df_occur_by_ctr('Italy').columns))
        self.assertIn(2015, al.df_occur_by_ctr('The Whole World').year.values)
        self.assertNotIn(1970, al.df_occur_by_ctr('Angola').year.values)  # No attacks in Angola in 1970


    def test_df_occur_by_ctr_allyears(self):
        '''
        test the df_occur_by_ctr_allyears function in AnalysisAndLinePlot module
        whether the return DataFrame is in expected format with correct values
        '''
        self.assertEqual(46, len(al.df_occur_by_ctr_allyears('France')))
        self.assertEqual(46, len(al.df_occur_by_ctr_allyears('Australia')))
        self.assertEqual(46, len(al.df_occur_by_ctr_allyears('Belgium')))
        self.assertEqual(46, len(al.df_occur_by_ctr_allyears('Mexico')))
        self.assertEqual(46, len(al.df_occur_by_ctr_allyears('The Whole World')))
        self.assertEqual(0, al.df_occur_by_ctr_allyears('Angola').occurrences[0])
        self.assertEqual(0, al.df_occur_by_ctr_allyears('Angola').loc[0, 'occurrences'])
        self.assertNotIn(2016, al.df_occur_by_ctr_allyears('United States').year.values)


    def test_gtd_country_names(self):
        '''
        test whether the gtd_country_names function in AnalysisAndLinePlot module
        returns the correct value
        '''
        self.assertEqual(207, len(al.gtd_country_names()))
        self.assertIn('Greece', al.gtd_country_names())
        self.assertIn('United States', al.gtd_country_names())
        self.assertNotIn('America', al.gtd_country_names())
        self.assertTrue('The Whole World', al.gtd_country_names()[0])


    def test_drop93(self):
        '''
        test whether the drop93 function in AnalysisAndLinePlot module
        returns a DataFrame without year 1993
        '''
        df_test93 = pd.DataFrame({'year': [1991, 1992, 1993, 1994, 1995],
                                  'value': ['1', '2', '3', '4', '5']})
        self.assertNotIn(1993, al.drop93(df_test93).year.values)
        self.assertIn(1994, al.drop93(df_test93).year.values)


    def test_df_ctr(self):
        '''
        test whether the df_ctr function in AnalysisAndLinePlot module
        returns a DataFrame only containing the data
        in the chosen country
        '''
        self.assertIn('Norway', al.df_ctr('Norway').country.values)
        self.assertNotIn('Sweden', al.df_ctr('Norway').country.values)
        self.assertNotIn('eventid', al.df_ctr('The Whole World').columns.values)


    def test_df_ctr_all(self):
        '''
        test whether the df_ctr_all function in AnalysisAndLinePlot module
        returns a DataFrame only containing the expected features of data
        in the chosen country
        '''
        self.assertIn('wounds', al.df_ctr_all('Japan').columns.values)
        self.assertNotIn('country', al.df_ctr_all('Japan').columns.values)
        self.assertEqual((45, 5), al.df_ctr_all('Japan').shape)


    def test_ctr_stats(self):
        '''
        test whether the ctr_stats function in AnalysisAndLinePlot module
        returns a DataFrame of analysis in the chosen country
        '''
        self.assertEqual(45, al.ctr_stats('South Korea').loc['year', 'count'])
        self.assertEqual(2015, al.ctr_stats('South Korea').loc['year', 'max'])
        self.assertIn('casualties', al.ctr_stats('Austria').index.values)
        self.assertIn('25%', al.ctr_stats('Austria').columns.values)


    def test_analy_ctr(self):
        '''
        test whether the analy_ctr function in AnalysisAndLinePlot module
        returns a string
        '''
        self.assertEqual(str, type(al.analy_ctr('Spain')))


    def test_analy_and_plot(self):
        '''
        test whether expected expectations for inputting invalid feature values
        '''
        with self.assertRaises(NoCountryDataError):
            al.analy_and_plot('America', 'wounds', 'white')  # should be 'United States' instead of 'America'
        # 'Korea' is not included in GTD database
        # however, there are 'South Korea' and 'North Korea'
        with self.assertRaises(NoCountryDataError):
            al.analy_and_plot('Korea', 'casualties', 'black')


    def test_choropleth(self):
        '''
        test the choropleth class and its methods
        '''
        chr_t1 = cr.Choropleth(Year=2011, Feature='casualties')
        # test the damage_by_year method
        self.assertEqual(1, chr_t1.damage_by_year().shape[1])
        self.assertIn('India', chr_t1.damage_by_year().index.values)
        # test the max_dam method
        self.assertEqual(6881, chr_t1.max_dam())
        # test the scale_max method
        self.assertGreater(chr_t1.scale_max(), chr_t1.max_dam())
        self.assertEqual(6900, chr_t1.scale_max())
        # test the all_ctr_dam method
        self.assertEqual(-99, chr_t1.all_ctr_dam().loc[3, 'casualties'])

        chr_t2 = cr.Choropleth(Year=2012, Feature='wounds')
        # test the damage_by_year method
        self.assertEqual(1, chr_t2.damage_by_year().shape[1])
        self.assertIn('Russia', chr_t2.damage_by_year().index.values)
        self.assertEqual(0, chr_t2.damage_by_year().loc['Germany', 'wounds'])
        # test the max_dam method
        self.assertEqual(6983, chr_t2.max_dam())
        # test the scale_max method
        self.assertGreater(chr_t2.scale_max(), chr_t2.max_dam())
        self.assertEqual(7000, chr_t2.scale_max())
        # test the all_ctr_dam method
        self.assertEqual(0, chr_t2.all_ctr_dam().loc[28, 'wounds'])
        self.assertEqual(-99, chr_t2.all_ctr_dam().wounds[chr_t2.all_ctr_dam().country == 'United Arab Emirates'].tolist()[0])


    def test_find_js_country_names(self):
        '''
        test the find_js_country_names function in the choropleth module
        '''
        self.assertEqual(180, cr.find_js_country_names().shape[0])
        self.assertEqual(np.ndarray, type(cr.find_js_country_names()))


    def test_js_country_names(self):
        '''
        test the js_country_names function in the choropleth module
        '''
        self.assertTrue(cr.js_country_names().shape == (180, 1))
        self.assertEqual('country', cr.js_country_names().columns.any())


    def test_plot_choropleth(self):
        '''
        test the plot_choropleth function in the choropleth module
        whether the expected errors would occur when invalid values are inputted
        '''
        # test when inputting year value outranging the dataset
        with self.assertRaises(NoDataError):
            cr.plot_choropleth(Color='cool', Feature='wounds', Year=2016)
        with self.assertRaises(NoDataError):
            cr.plot_choropleth(Color='Blues', Feature='kills', Year=1919)
    

    def test_plot_2D_density(self):
        '''
        test the plot_2D_density funtion in the Geo2D module
        whether the expections caused by inputting invalid year interval are catched properly
        '''
        # test whether the invalid inputs would cause expected NotIntervalError
        with self.assertRaises(NotIntervalError):
            geo.plot_2D_density(Year=2009, MapStyle='Plain')
        with self.assertRaises(NotIntervalError):
            geo.plot_2D_density(Year='foo', MapStyle='Plain')
        with self.assertRaises(NotIntervalError):
            geo.plot_2D_density(Year=[1990, 1992, 1999], MapStyle='Plain')

        # test whether the exceeded interval woud cause expected IntervalLeakError
        with self.assertRaises(IntervalLeakError):
            geo.plot_2D_density(Year=(2000, 2016), MapStyle='Plain')
        with self.assertRaises(IntervalLeakError):
            geo.plot_2D_density(Year=(1933, 1988), MapStyle='Plain')

        # test whether the expected error would occur
        # when the interval starting value is greater than the ending value
        with self.assertRaises(IntervalReverseError):
            geo.plot_2D_density(Year=(2000, 1996), MapStyle='Plain')


    def test_GTA(self):
        '''
        test the GTA class with its attributes and methods in the heatmap module
        '''
        gta = ht.GTA()
        # test the attibute
        self.assertIn('South Asia', gta.region_names)
        self.assertEqual(12, len(gta.region_names))

        # test the methods
        ctr_dict = gta.countries_by_region()
        self.assertEqual(dict, type(ctr_dict))
        self.assertIn('Australasia & Oceania', ctr_dict.keys())
        self.assertTrue(np.ndarray, type(ctr_dict['East Asia']))
        self.assertIn('Vatican City', ctr_dict['Western Europe'])


if __name__ == "__main__":
    unittest.main()
