'''
This module contains user's self-defined exceptions.

@author: Xianzhi Cao (xc965)
'''

# Error: Data not available in this year.
class NoDataError(Exception):
    def __str__(self):
        return 'No available data from Global Terrorism Database in this year.\n'


# Error: Data not available in this country.
class NoCountryDataError(Exception):
    def __str__(self):
        return 'No available data from Global Terrorism Database in this country.\n'


# Error: Loading Non-json file error
class LoadJsonError(Exception):
    def __str__(self):
        return 'This is not a json file!\n'
