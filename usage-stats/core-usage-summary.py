#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:45:33 2020

Python 3

@author: khs3z
"""

from __future__ import print_function
import pandas as pd
import argparse

pd.options.display.float_format = '{:,.2f}'.format

def init_parser():
    parser = argparse.ArgumentParser(
        description='Parses SLURM core hour usage, mam account and mam organization information to create Rivanna usage stats')
    parser.add_argument('-a', '--allocations', help='file with allocation informaton')
    parser.add_argument('-c', '--core-usage', help='file with core hour usage')
    parser.add_argument('-x', '--organizations', help='file with mam organization info')
    parser.add_argument('-o', '--output', help='output file')
    return parser


def merge_data(usage_file, account_file, org_file):
    usage_df = pd.read_csv(usage_file, delimiter=',', names=['Allocation', 'Total CPU hours']) #, header=0, skiprows=7)
    account_df = pd.read_csv(account_file, delimiter=r"\s+", header=0)
    org_df = pd.read_csv(org_file, delimiter=r"\s+", header=0, names=['Organization', 'School'])
 
    cols = account_df.columns.values
    cols[0] = "Allocation"
    account_df.columns = cols

    accts_and_orgs = pd.merge(account_df, org_df, on='Organization', how='outer', suffixes=('_left', '_right'))

    combined = pd.merge(usage_df, accts_and_orgs, on='Allocation', how='left', suffixes=('_left', '_right'))
    return combined


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args() 
    df = merge_data(args.core_usage, args.allocations, args.organizations)

    df.to_csv(args.output, index=False)
    groups = ['BII','SEAS','CLAS','SDS','SOM','Other']
    dfs = [df[df.School==group] for group in groups]

    print (df.groupby("School").sum())  
    print ("------------------------------------")
    print (f"Total Hours: {df['Total CPU hours'].sum():,.2f}")
