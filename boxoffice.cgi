#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Provides plotting functions for BoxOfficeMojo data

Example usage: <URL>/boxoffice.py?id=et,titanic&type=c
"""

import cgi
from boxofficemojo import retrieve_incomes
from googlechart import create_chart

__author__ = "Claudio Baccigalupo"


def main():
    form = cgi.FieldStorage()
    if form.has_key("id"):
        movie_ids  = form["id"].value.split(",")
    else:
        movie_ids  = ["slumdogmillionaire", "neverbeenkissed"]

    full_weeks = [form.has_key("w")] * len(movie_ids)
    use_cumes  = [form.has_key("c")] * len(movie_ids)
    
    incomes = map(retrieve_incomes, movie_ids, full_weeks, use_cumes)
    
    chart_url = create_chart(incomes)

    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    print "<title>Box Office Plot</title>\n"
    print "<img src=\"%s\" />\n" % chart_url
    
main()