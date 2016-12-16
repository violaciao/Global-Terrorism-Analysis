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
from data import *
from UserError import *

'''
Common Assertions

Method
assertTrue(x, msg=None)
assertFalse(x, msg=None)
assertIsNone(x, msg=None)
assertIsNotNone(x, msg=None)
assertEqual(a, b, msg=None)
assertNotEqual(a, b, msg=None)
assertIs(a, b, msg=None)
assertIsNot(a, b, msg=None)
assertIn(a, b, msg=None)
assertNotIn(a, b, msg=None)
assertIsInstance(a, b, msg=None)
assertNotIsInstance(a, b, msg=None)
assertAlmostEqual(a, b, places=7, msg=None, delta=None)
assertNotAlmostEqual(a, b, places=7, msg=None, delta=None)
assertGreater(a, b, msg=None)
assertGreaterEqual(a, b, msg=None)
assertLess(a, b, msg=None)
assertLessEqual(a, b, msg=None)
assertRegex(text, regexp, msg=None)
assertNotRegex(text, regexp, msg=None)
assertCountEqual(a, b, msg=None)
assertMultiLineEqual(a, b, msg=None)
assertSequenceEqual(a, b, msg=None)
assertListEqual(a, b, msg=None)
assertTupleEqual(a, b, msg=None)
assertSetEqual(a, b, msg=None)
assertDictEqual(a, b, msg=None)
'''


class UserTest(unittest.TestCase):
    """
    This class allows users to run tests with classes and functions.
    """

    def setUp(self):
        pass


    # def test_make_df(self):
    #     '''
    #     test the make_df function in the data module
    #     whether returns the correct DataFrames
    #     '''
    #     # test if the appended feature name 'casualties' is in the column names
    #     self.assertTrue('casualties' in make_df().columns.tolist())
    #     # test whether the length of DataFrame is greater than 150,000
    #     self.assertGreater(make_df().shape[0], 150000)
    #
    #
    # def test_load_json_file(self):
    #     '''
    #     test the load_json_file function in the data module
    #     whether the expected exceptions and errors occurred
    #     when non-json file is uploaded
    #     '''
    #     test_path = 'gtd_wholedata.csv'
    #     # test when year input is emtpy
    #     with self.assertRaises(LoadJsonError):
    #         load_json_file(filepath=test_path)
    #
    #
    # def test_make_array(self):
    #     '''
    #     test the make_array function in the util module
    #     whether the correct income lists are returned
    #     '''
    #     df_test1 = pd.read_csv('https://bit.ly/uforeports')
    #     self.assertEqual(np.ndarray, type(ut.make_array(df_test1, 'City')))
    #
    #
    # def test_df_sel_btw_years(self):
    #     '''
    #     test the df_sel_btw_years function in util module
    #     whether the output DataFrame is in the expected time range
    #     '''
    #     self.assertTrue(2002 in list(ut.df_sel_btw_years((2000, 2005)).year))
    #     self.assertFalse(1990 in list(ut.df_sel_btw_years((2000, 2005)).year))
    #
    #
    # def test_make_five_year_start(self):
    #     '''
    #     test the make_five_year_start function in the util module
    #     whether the values in the new feature 'period'
    #     can be devided by 5.
    #     '''
    #     df3 = ut.make_five_year_start(load_df())
    #     self.assertTrue('period' in df3)
    #     self.assertTrue(2000 in list(df3[df3.year.isin([2001, 2002, 2004])].period))
    #     self.assertNotIn(2005, list(df3[df3.year.isin([2001, 2002, 2004])].period.values))
    #
    # #################
    #
    # # Caroline's test goes here
    #
    # #################
    #
    #
    # def test_df_occur_by_ctr(self):
    #     '''
    #     test the df_occur_by_ctr function in AnalysisAndLinePlot module
    #     whether the return DataFrame is in expected format with correct values
    #     '''
    #     self.assertEqual(['year', 'occurrences'], list(al.df_occur_by_ctr('Germany').columns))
    #     self.assertEqual(['year', 'occurrences'], list(al.df_occur_by_ctr('The Whole World').columns))
    #     self.assertEqual(pd.Index, type(al.df_occur_by_ctr('Italy').columns))
    #     self.assertIn(2015, al.df_occur_by_ctr('The Whole World').year.values)
    #     self.assertNotIn(1970, al.df_occur_by_ctr('Angola').year.values)  # No attacks in Angola in 1970
    #
    #
    # def test_df_occur_by_ctr_allyears(self):
    #     '''
    #     test the df_occur_by_ctr_allyears function in AnalysisAndLinePlot module
    #     whether the return DataFrame is in expected format with correct values
    #     '''
    #     self.assertEqual(46, len(al.df_occur_by_ctr_allyears('France')))
    #     self.assertEqual(46, len(al.df_occur_by_ctr_allyears('Australia')))
    #     self.assertEqual(46, len(al.df_occur_by_ctr_allyears('Belgium')))
    #     self.assertEqual(46, len(al.df_occur_by_ctr_allyears('Mexico')))
    #     self.assertEqual(46, len(al.df_occur_by_ctr_allyears('The Whole World')))
    #     self.assertEqual(0, al.df_occur_by_ctr_allyears('Angola').occurrences[0])
    #     self.assertEqual(0, al.df_occur_by_ctr_allyears('Angola').loc[0, 'occurrences'])
    #     self.assertNotIn(2016, al.df_occur_by_ctr_allyears('United States').year.values)
    #
    #
    # def test_gtd_country_names(self):
    #     '''
    #     test whether the gtd_country_names function in AnalysisAndLinePlot module
    #     returns the correct value
    #     '''
    #     self.assertEqual(207, len(al.gtd_country_names()))
    #     self.assertIn('Greece', al.gtd_country_names())
    #     self.assertIn('United States', al.gtd_country_names())
    #     self.assertNotIn('America', al.gtd_country_names())
    #     self.assertTrue('The Whole World', al.gtd_country_names()[0])
    #
    #
    # def test_drop93(self):
    #     '''
    #     test whether the drop93 function in AnalysisAndLinePlot module
    #     returns a DataFrame without year 1993
    #     '''
    #     df_test93 = pd.DataFrame({'year': [1991, 1992, 1993, 1994, 1995],
    #                               'value': ['1', '2', '3', '4', '5']})
    #     self.assertNotIn(1993, al.drop93(df_test93).year.values)
    #     self.assertIn(1994, al.drop93(df_test93).year.values)


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
        self.assertEqual(45, al.ctr_stats('Korea').loc['year', 'count'])
        self.assertEqual(2015, al.ctr_stats('Korea').loc['year', 'max'])

        self.assertEqual(45, al.ctr_stats('Korea').loc['year', 'count'])








if __name__ == "__main__":
    unittest.main()
