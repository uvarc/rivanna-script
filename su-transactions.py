#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:43:24 2020

Parses the SU transactions saved as html file from https://rci.hpc.virginia.edu/rc/alloc_transaction.php'

@author: khs3z
"""

from __future__ import print_function
import argparse
from bs4 import BeautifulSoup
import pandas as pd


def init_parser():
    parser = argparse.ArgumentParser(
        description='Parses an html file obtained from https://rci.hpc.virginia.edu/rc/alloc_transaction.php')
    parser.add_argument('-f', '--file', help='html file with tabular data')
    parser.add_argument('-s', '--start', default=None, help='reporting start date YYYY-MM-DD')
    parser.add_argument('-e', '--end', default=None, help='reporting end date YYYY-MM-DD')
    parser.add_argument('-g', '--group', default=None, type=str, help='comma separated list of columns to group data by, e.g. "School,Type"')
    parser.add_argument('-x', '--exclude', default='transfer', type=str, help='comma separated list of transaction types to exclude')
    return parser


def read_data(args):
    with open(args.file, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html5lib')
        # parse table headers and body
        headers = [th.text for th in soup.find_all('th')]
        data = [[i.text for i in tr.find_all('td')] for tr in soup.find_all('tr')]
        #create dataframe and set column data types
        df = pd.DataFrame(data, columns=headers)
        df['Amount'] = pd.to_numeric(df['Amount'])
        df['Date']= pd.to_datetime(df['Date'])
        return df
    return None


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    df = read_data(args)
    if df is not None:
        # drop transaction types to exclude
        if args.exclude is not None:
            df = df[~df['Type'].isin(args.exclude.split(','))]
        # filter by start and end date
        if args.start is not None:
            df = df[df['Date'] >= args.start]
        if args.end is not None:
            df = df[df['Date'] <= args.end]
        # group data
        if args.group is not None:
            groups = args.group.split(',')
            columns = ['Amount']
            columns.extend(groups)
            columns = set(columns)
            df = df[columns].groupby(groups).agg(['sum','count'])
        print (df)
    else:
        print ("No data or processing error. ")