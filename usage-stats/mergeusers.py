#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
Created on Sun Sep 13 21:32:40 2020

@author: khs3z
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 09:52:13 2020

@author: khs3z
"""


import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import sys

path = '' #'/Users/khs3z/Documents/ARCS/Annual Reports/Office Hours/'
#uidfile = os.path.join(path, 'rivanna-newusers-full-2021-Mar.txt')#'OfficeHoursUserInfo.csv')
uidfile = sys.argv[1]
#userfile = os.path.join(path, 'rivanna-users-2020-Oct.csv') #'Office Hours Attendees.csv')
outputfile = os.path.join(path, 'Combined_'+os.path.basename(uidfile))
officehours = os.path.join(path, 'Combined_Office Hours Attendees-curated.csv')
report = os.path.join(path, 'Office_Hours_Attendees-report.xlsx')

schools = {'CLAS': ['e0:as', 's0:as', 's1:as', 's3:as', 'arts', 'global public health', 'english','economics', 'psychology', 'environmental', 'politics', 'biology', 'chemistry'], 
           'SEAS': ['e0:en', 's0:en', 's1:en', 's2:en','engineer', 'systems', 'computer', 'materials'], 
           'SOM': ['e0:interns and  resident','e0:md', 'som', 'global health', 'cphg', 'physical therapy', 'public health genomics', 'public health science', 'public health services', 'pharma', 'md-micr', 'biomed', 'infect', 'neuroscience', 'medicine', 'cardiovascular', 'cell bio', 'pediatrics', 'immunology', 'microbio'],
           'SDS': ['data', 'dsi', 'sds', 'e0:ds'],
           'DARD': ['da:', 'e0:da', 'darden', 'business'],
           #'Provost\'s Office': ['provost'],
           'SEHD': ['ed:', 'education', 'teaching'],
           #'RDS (Library)': ['e0:lb', 'library'],
           #'Health Sciences Library': ['hsl'],
           'COMM': ['e0:mc', 'mcintire', 'commerce', 'mc-'],
           'SON': ['nursing'],
           'BATT': ['e0:cu-leadshp','batten'],
           'ITS/RC': ['e0:it-research computing', 'research-computing'],
           'BII': ['e0:pv-bii', 's0:pv-bii', 'biocomplexity'],
           'PROV': ['pv-'],}

def lookup_school(df):
    depthit = (s for s in schools for entry in schools[s] if entry in df['Dept'].lower())
    try:
        return depthit.next()
    except:
        affilhit = (s for s in schools for entry in schools[s] if entry in df['Affiliation'].lower())
        try:
            affil = affilhit.next() 
            return affil
        except:
            return 'OTHER'


uid_df = pd.read_csv(uidfile, names=["UserID", "Lastname", "Firstname", "Affiliation", "Status"])
#uid_df.set_index([0]);
#print (uid_df.head())

#user_df = pd.read_csv(userfile, delimiter=',', header=None, names=["UserID","Active","CommonName","PhoneNumber","EmailAddress","DefaultAccount","Description","CreationTime","ModificationTime","Deleted","RequestId","TransactionId"])
#print (user_df.head())

#combined = pd.merge(user_df, uid_df, on='UserID', how='left', suffixes=('_left', '_right'))
#print (combined.head())

uid_df['School'] = uid_df.apply(lookup_school, axis=1)
uid_df.to_csv(os.path.join(path,outputfile))
print (uid_df)
print ('-------------------------------------------')
