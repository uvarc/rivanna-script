#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:45:33 2020

Python 3

@author: khs3z
"""

from __future__ import print_function
import pandas as pd
import argparse
import re

pd.options.display.float_format = '{:,.2f}'.format

def init_parser():
    parser = argparse.ArgumentParser(
        description='Parses SLURM core hour usage, mam account and mam organization information to create Rivanna usage stats')
    parser.add_argument('-a', '--allocations', required=True, help='file with allocation informaton')
    parser.add_argument('-c', '--core-usage', required=True, help='file with core hour usage')
    parser.add_argument('-x', '--organizations', required=True, help='file with mam organization info')
    parser.add_argument('-o', '--output', required=True, help='output file')
    parser.add_argument('-l', '--labels', required=True, default='Allocation,Total CPU hours', help='comma separated list of core usage columns')
    return parser

def calc_gpu_hours(row):
    if row['alloccpus'] != 0:
        return row['GPU devices'] * row['Total CPU hours'] / row['alloccpus']
    else:
        return 0.0

def merge_data(labels, usage_file, account_file, org_file):
    labels = labels.split(',')
    #usage_df = pd.read_fwf(usage_file, widths=[11,51,11,11,11,11], names=labels) #, header=0, skiprows=7)
    usage_df = pd.read_csv(usage_file, delimiter="|")#r"\s+", names=labels) #, header=0, skiprows=7)
    #print (usage_df.head())
    usage_df['Total CPU hours'] = usage_df['cputimeraw']/3600 
    usage_df['GPU devices'] = usage_df['alloctres'].str.extract(r'gres/gpu=(\d+)').fillna(0).astype(int)#.apply(lambda row:get_gpu_devices(row), axis=1)
    #print (usage_df.head())
    usage_df['Total GPU hours'] = usage_df.apply(lambda row: calc_gpu_hours(row), axis=1)
    #usage_df = usage_df.groupby(['user','Allocation',]).sum().reset_index()
    usage_df = usage_df.groupby(['Allocation',]).sum().reset_index()
    #print (usage_df.head())

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
    df = merge_data(args.labels, args.core_usage, args.allocations, args.organizations)
    print (df.head())

    df.to_csv(args.output, index=False)
    groups = ['BII','SEAS','CLAS','SDS','SOM','Other']
    dfs = [df[df.School==group] for group in groups]

    print (df.groupby("School").sum())  
    print ("------------------------------------")
    print (f"Total CPU Hours: {df['Total CPU hours'].sum():,.2f}")
    print (f"Total GPU Device Hours: {df['Total GPU hours'].sum():,.2f}")

