'''
This module contains user's self-defined exceptions.

Module Author: Xianzhi Cao (xc965)
Project co-author: Caroline Roper (cer446)
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


# Error: Loading the wrong excel file error
class WrongDatafileError(Exception):
    def __str__(self):
        return 'Please use the offical dataset by GTD following the User Manual!\n'


# Error: Input is not a year interval
class NotIntervalError(Exception):
    def __str__(self):
        return 'This is not an year interval!\n'


# Error: Ending year is greater than the starting
class IntervalReverseError(Exception):
    def __str__(self):
        return 'Please switch your starting and ending year!\n'


# Error: Year interval leaking the bounds
class IntervalLeakError(Exception):
    def __str__(self):
        return 'Interval bounds Leakage! Please enter a list of year interval between 1970 and 2015.\n'
