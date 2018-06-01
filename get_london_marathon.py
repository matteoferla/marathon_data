#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__description__ = \
    """
A script for Giuseppe to download all the London marathon data.
NB. Written for python 3, not tested under 2.
"""
__author__ = "Matteo Ferla. [Github](https://github.com/matteoferla)"
__email__ = "matteo.ferla@gmail.com"
__date__ = ""
__license__ = "Cite me!"
__version__ = "1.0"

import csv, os
import urllib.request
from warnings import warn

from bs4 import BeautifulSoup

for year in range(2018, 2019):
    with open("marathon_{year}.csv".format(year=year), "w") as f:
        for page in range(1, 1415):
            # get data
            if year > 2013:
                url = 'http://results-{year}.virginmoneylondonmarathon.com/{year}/?page={page}&event=MAS&num_results=1000&pid=search&search%5Bsex%5D=%25&search%5Bnation%5D=%25&search_sort=name'.format(
                    page=page, year=year)
            elif year > 2009:
                url = 'http://results-{year}.virginlondonmarathon.com/{year}/index.php?page={page}&event=MAS&num_results=1000&pid=search&search%5Bsex%5D=%25&search_sort=place_nosex&split=time_finish_netto'.format(
                    page=page, year=year)
            elif year == 2009:  # actually it cannot download 1,000 at a time. so the page number should be 1414
                url = 'http://results-2009.london-marathon.co.uk/index.php?lastname=&firstname=&club=&gender=&num_results=1000&nation=&event_id=MAS&start_no=&position=&split=FINISHNET&Submit=show+results+%3E%3E&a=s&p={page}'.format(
                    page=page, year=year)
            else:
                warn('The format for the year {0} is unknown'.format(year))
                break
            # save date
            fname = 'pages/marathon_{year}.p{page}.html'.format(page=page, year=year)
            if os.path.isfile(fname):
                print(year, page,'cache')
                fp = open(fname)
                html=fp.read()
            else:
                print(year, page,'download')
                html = str(urllib.request.urlopen(url).read(), 'utf-8')
                fp = open(fname, 'w')
                fp.write(html)
            if (html.find('No results found') != -1 or html.find('no results found') != -1):
                if html.find('Sorry, no results found!') == -1:
                    break
            # parse data
            soup = BeautifulSoup(html.replace('\n', ''), "html.parser")
            table = soup.select_one("table.list-table")
            if page == 1:
                headers = [th.text.replace(" ","").title() for th in table.select("tr th")]
                wr = csv.writer(f)
                wr.writerow(headers)
            wr.writerows([[td.text.replace('&#187; ', '').replace('Â» ', '').replace('» ', '') for td
                           in row.find_all("td")] for row in table.select("tr")])
