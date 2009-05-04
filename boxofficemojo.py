#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Provides function to retrieve incomes from BoxOfficeMojo

Example usage: ./boxofficemojo.py -c titanic
"""

import sys
import re
import logging
from optparse import OptionParser

from download import download_page

__author__ = "Claudio Baccigalupo"

def retrieve_incomes(movie_id, full_week=False, use_cumes=False): 
    '''Retrieve income data for movie_ids from BoxOfficeMojo.'''

    def parse_incomes(page, full_week, use_cumes):
        '''Parse BoxOfficeMojo page for movie incomes.'''
        if use_cumes:
            if full_week:
                pattern = r'<font color="#800080" size="2">\$([0-9,]*?) / ([0-9]*?)</font>'
            else:
                pattern = r'<td align="right"><font size="2">\$([0-9,]*?)</font></td><td align="center"><font size="2">([0-9]*?)</font></td></tr>'
            incomes = [g[0] for g in re.findall(pattern, page)]
        else:
            if full_week:
                pattern = r'<font color="#000080">\$([0-9,]*?)</font>'
                incomes =  re.findall(pattern, page)
            else:
                pattern = r'<td align="center"><font size="2">([0-9\-]*?)</font></td><td align="right"><font size="2">\$([0-9,]*?)</font></td>'
                incomes =  [g[1] for g in re.findall(pattern, page)]
        return [int(g.replace(",","")) for g in incomes]
        
        
    url_template = "http://www.boxofficemojo.com/movies/?page=%s&id=%s.htm"
    if full_week:
        url = url_template % ("daily", movie_id)
    else:
        url = url_template % ("weekend", movie_id)
    resp = download_page(url)
    if resp is None:
        logging.warning("BoxOfficeMojo movie not found: %s" % url)
    else:
        return {'id': movie_id, 'values': parse_incomes(resp, full_week, use_cumes)}

def main(argv=None):
    
    usage = "usage: %prog [options] movie_id"
    parser = OptionParser(usage)
    parser.add_option("-w", "--week", dest="full_week", default=False,
                      action="store_true", help="return day-by-day incomes")
    parser.add_option("-c", "--cume", dest="use_cumes", default=False,
                      action="store_true", help="return cumulative incomes")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("No movie was specified")

    return retrieve_incomes(args[0], opts.full_week, opts.use_cumes)

if __name__ == "__main__":
    sys.exit(main())
