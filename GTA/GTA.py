'''
Created on Nov 7, 2016

We should write all the procedures, including packing installing, data downloading, etc. into the user's manual;
we also need to write specific guidance of all the functions about the program.

Write clean code, look at the documentations and use multiple functions to show our capabilities.

Important: We should put emphasis on the data ANALYSING part as well!

Finally, test the program, and make sure all tests are passed.
Test modules should be put under the top level of the project directory.

Module Author: Xianzhi Cao (xc965)
Project co-author: Caroline Roper (cer446)
'''


import AnalysisAndLinePlot as al
import heatmap as ht
import choropleth as cr
import Geo2D as geo
import bubble_chart as bc
import dot_plot as dot


def GTA_AL():
    return al.Display_Your_Analysis_And_LinePlot()


def GTA_CHR():
    return cr.Display_Your_Choropleth()


def GTA_HT():
    return ht.Display_Your_Heatmap()


def GTA_GEO():
    return geo.Display_Your_Geo2D_Map()


def GTA_BC():
    return bc.Display_Your_Bubble_Chart()


def GTA_DOT():
    return dot.Display_Your_Dot_Plot()
