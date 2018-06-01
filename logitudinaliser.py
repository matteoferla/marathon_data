#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__description__ = \
    """

NB. Written for python 3, not tested under 2.
"""
__author__ = "Matteo Ferla. [Github](https://github.com/matteoferla)"
__email__ = "matteo.ferla@gmail.com"
__date__ = ""
__license__ = "Cite me!"
__version__ = "1.0"

import csv, os, re
from collections import defaultdict

# Place Overall, Place Gender, Place Category, Name , BIB, Category, HALF, Finish time,
#2,2,2,"Mutai, Emmanuel (KEN)",7,18-39,01:03:06,02:06:23,


xdb=defaultdict(list)
for year in range(2010,2019):
    with open('marathon_{}.csv'.format(year)) as fh:
        for arrival in csv.DictReader(fh):
            if arrival['Name']: #no nameless folk
                arrival['Year']=year
                xdb[arrival['Name']].append(arrival)

cats=['18-39','40-44','45-49','50-54','55-59','60-64','65-69','70+','']
print('Runners:',len(xdb))

db=[[] for i in range(10)]
doublerunners=[0]*100
benjamins=[0]*100 #B. Button
for runner in xdb:
    try:
        yball=[a['Year'] for a in xdb[runner]]
        if len(yball) != len(set(yball)): #no doublerunnings!
            doublerunners[len(xdb[runner])]+=1
            continue
        mycat=[cats.index(a['Category']) for a in xdb[runner] if a['Category']]
        t=False
        o=0
        for c in mycat:
            if c == 8:  #redundant
                continue
            if c < o:
                t=True
            o=c
        if mycat and (max(mycat)-min(mycat) > 3 or t):
            benjamins[len(xdb[runner])]+=1
            continue
        db[len(xdb[runner])].extend(xdb[runner])
    except Exception as e:
        print(runner)
        print(xdb[runner])
        raise e

print(doublerunners)
print(benjamins)

for i in range(10):
    print(i, len(db[i]),len({a['Name'] for a in db[i]}))
    if len(db[i]):
        with open('logitudinal_x{}.csv'.format(i),'w') as fh:
            w=csv.DictWriter(fh,'Year,Placeoverall,Placegender,Placecategory,Name,Club,Runnerno,Category,Half,Finish,'.split(','))
            w.writeheader()
            w.writerows(db[i])

