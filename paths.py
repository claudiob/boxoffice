#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Provides plotting functions for BoxOfficeMojo data

Example usage: ./paths.py -c once
"""

import sys
import getopt
import os
import re
import logging
import webbrowser

from utils import *
from download import *

__author__ = "Claudio Baccigalupo"

def plot(movie_id, full_week=False, use_cumes=False): 
    values = parse(movie_id, full_week, use_cumes)
    chart_url = "http://chart.apis.google.com/chart?"
    chart_url = chart_url + "chs=1000x300" # Width
    chart_url = chart_url + "&chtt=U.S.+Weekend+Gross&chts=FF0000,20" # Title
    chart_url = chart_url + "&chdl=" + movie_id # Legend
    chart_url = chart_url + "&chxt=x,y" # Axis type
    chart_url = chart_url + "&chxl=0:|1||||5|||||10|||||15|||||20|||||" + \
                            "25|||||30|||||35|||||40|||||45|||||50" + \
                                  "1:|0|500|1000" # Axis labels
    chart_url = chart_url + "&chxr=0,1,50|1,0,1000" # Axis range
    chart_url = chart_url + "&cht=bvg" # Bar charts
    chart_url = chart_url + "&chbh=a" # Bar charts width
    chart_url = chart_url + "&chco=4D89F9" # Colors
    # If relative:
    chart_url = chart_url + "&chds=0," + values[-1] # Data scaling
    # Else:
    #chart_url = chart_url + "&chds=0,700000000" # Data scaling
    # Data
    chart_url = chart_url + "&chd=t:"
    chart_url = chart_url + ",".join(values)
    webbrowser.open(chart_url)
    return values
    
    

def parse(movie_id, full_week=False, use_cumes=False): 
    '''Return list of friends and, if not only_id, page count and is artist.'''

    def parse_grosses(page, full_week):
        '''Returns the list of friend IDs in the page.'''
        if full_week:
            daily_pattern = r'<font color="#000080">\$([0-9,]*?)</font>'
            grosses =  re.findall(daily_pattern, page)
        else:
            weekend_patterns = r'<td align="center"><font size="2">([0-9]*?)</font></td><td align="right"><font size="2">\$([0-9,]*?)</font></td>'
            grosses =  re.findall(weekend_patterns, page)
            grosses = [g[1] for g in grosses]
        return [g.replace(",","") for g in grosses]
        
    def parse_cumes(page, full_week):
        if full_week:
            daily_pattern = r'<font color="#800080" size="2">\$([0-9,]*?) / ([0-9]*?)</font>'
            cumes =  re.findall(daily_pattern, page)
            cumes = [c[0] for c in cumes]
        else:
            weekend_patterns = r'<td align="right"><font size="2">\$([0-9,]*?)</font></td><td align="center"><font size="2">([0-9]*?)</font></td></tr>'
            cumes =  re.findall(weekend_patterns, page)
            cumes = [c[0] for c in cumes]
        return [c.replace(",","") for c in cumes]
        
    url_template = "http://www.boxofficemojo.com/movies/?page=%s&id=%s.htm"
    if full_week:
        url = url_template % ("daily", movie_id)
    else:
        url = url_template % ("weekend", movie_id)
    resp = download_page(url)
    if resp is None:
        logging.debug("URL error on: %s" % url)
    else:
        if use_cumes:
            return parse_cumes(resp, full_week)
        else:
            return parse_grosses(resp, full_week)

    
def main(argv=None):

    def usage():
        # Add an interactive version to add parameters one by one
        print ("Usage: %s movietitle" % argv[0])
        print ("   options:")
        print ("   -h [--help] print this usage statement")
        print ("   -w [--week] print full week (not weekend")
        print ("   -c [--cumes] print cumulatives")
        return

    movie_title    = None
    log_path       = None
    full_week      = False
    use_cumes      = False
    logging_config = {"level": logging.INFO}
    if argv is None:
        argv = sys.argv
    try:
        ###### 1. Retrieve opts and args #####
        try:
            opts, args = getopt.getopt(argv[1:], "hwc", ["help", "week", "cumes"])
        except getopt.error, msg:
             raise Usage(msg)
        ###### 2. Process opts ###### 
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-w", "--week"):
                full_week = True
            elif opt in ("-c", "--cumes"):
                use_cumes = True
        ###### 3. Process args ######
        if len(args) < 1:
            raise Usage("You did not specify a movie ID")
        elif len(args) > 1:
            raise Usage("You specified more than one movie ID")
        else:
            movie_title = args[0]
        ###### 4. Enable logging ######
        logging_config["format"] = '%(asctime)s %(levelname)-8s %(message)s'
        logging_config["datefmt"] = '%Y/%M/%D %H:%M:%S'
        if log_path is not None:        
            logging_config["filename"] = os.path.join(log_path, "movie.log")
            logging_config["filemode"] = "w"
        logging.basicConfig(**logging_config)
        ###### 5. Plot data ######
        result = plot(movie_title, full_week, use_cumes)
        return result
    ###### Manage errors ######
    except Usage, err:
        print >>sys.stderr, err.msg
        usage()
        return 2

if __name__ == "__main__":
    sys.exit(main())
