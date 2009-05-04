#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Provides interface to Google Chart API

Example usage: ./googlechart.py [{'id': 'one', 'data': [1,2,3]}]
"""

import sys
import getopt
import os
import re
import logging
import webbrowser
import urllib
import locale

from download import *

__author__ = "Claudio Baccigalupo"

def create_chart(items):
    # Items are hash of the form {'id': [name], 'values': [values]}
    items     = [i for i in items if i['values']] # Remove empty items
    if not items:
        return
    titles    = [i['id'] for i in items]
    values    = [i['values'] for i in items]
    max_value = max(map(max, values))
    max_ylab  = 10**(len(str(max_value))-1)

    locale.setlocale(locale.LC_ALL, 'en_US') # format y values in dollars
    xlab = "|".join(["||||%d" % n for n in range(5,100,5)])
    ylab_pos = ",".join([str(n) for n in [0] + range(max_ylab, max_value, max_ylab)])
    ylab = "|".join([locale.format("%d", int(n), True) + " $" for n in ylab_pos.split(",")])
    
    def value_to_string(value): 
        return ",".join(map(str, value))

    colors = ["AA0000", "AAAA00", "00AA00", "00AAAA", "0000AA", "AA00AA"]
    width=1000
    height=300
    title=""
    title_color="FF0000"
    title_size=20
         
    url =  "http://chart.apis.google.com/chart?cht=bvg"
    url += "&chxt=x,y" # Axis type
    url += "&chbh=a"   # Bar charts width
    url += "&chs=%dx%d" % (width, height)
    url += "&chxl=0:|1%s|1:|%s" % (xlab, ylab)
    url += "&chxp=1,%s" % ylab_pos
    url += "&chxr=0,1,100|1,0,%d" % max_value # Axis range
    if title != "":
        url += "&chtt=%s" % urllib.quote_plus(title)
        url += "&chts=%s,%d" % (title_color, title_size)
    url += "&chco=" + ",".join(colors[0:len(values)])
    url += "&chdl=" + "|".join(titles)
    url += "&chds=0,%d" % max_value
    url += "&chd=t:" + "|".join(map(value_to_string, values))
    
    return url[0:2047] # Not the right fix; values should be limited before
    
    