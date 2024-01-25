#!/usr/bin/env python

import numpy as np
import pandas as pd
import argparse
import re
import os

pd.options.display.float_format = '{:,.2f}'.format


def init_parser():
	parser = argparse.ArgumentParser(
		description='Parses SLURM core hour usage, mam account and mam organization information to create Rivanna usage stats')
	parser.add_argument('-a', '--allocations', required=True, help='file with allocation information')
	parser.add_argument('-u', '--usage', required=True, help='file with core hour usage')
	parser.add_argument('-c', '--capacity', required=False, help='file with core and GPU device counts for each partition')
	parser.add_argument('-x', '--organizations', required=True, help='file with mam organization info')
	parser.add_argument('-o', '--output', required=True, help='output file')
	parser.add_argument('-g', '--groups', required=False, default='School')
	parser.add_argument('-d', '--days', required=True, help='reporting period in days')
	parser.add_argument('-l', '--labels', required=False, default='Allocation,Total CPU hours', help='comma separated list of core usage columns')
	parser.add_argument('-f', '--filter', required=True, help='filter')
	parser.add_argument('-p', '--path', required=False, help='file path')
	return parser


def calc_gpu_hours(row):
	if row['alloccpus'] != 0:
		return row['GPU devices'] * row['Total CPU hours'] / row['alloccpus']
	else:
		return 0.0


def job_type(row):
	jtype = row['JobName']
	if jtype.startswith('ood_'):
		jtype = f'interactive ({row["JobName"]})'
	elif jtype.startswith('sys/dashboard'):
		jtype = f'interactive (ood_{row["JobName"].split("/")[-1]})'
	elif 'interactive' in jtype:
		jtype = 'interactive (not OOD)'
	else:
		jtype = 'non-interactive slurm'
	jtype = jtype.replace('rstudio_server', 'rstudio')
	jtype = jtype.replace('jupyter_lab', 'jupyter')
	return jtype


def job_state(row):
	return row['state'].split(' ')[0]


def gpu_devices(row):
	# devices = 0
	pattern = r'gpu\:.*?\:(\d+)'
	matches = re.findall(pattern, row['GRES'])
	return sum(int(m) for m in matches)


def utilization(row, cap_dict):
	partition = row['partition']
	if 'gpu' in partition:
		util = row['Total GPU hours'] / (cap_dict[partition]['GPU hours'])
	else:
		util = row['Total CPU hours'] / (cap_dict[partition]['Core hours'])
	return util


def partition_type(row):
	if row['partition'] in ['instructional', 'eqa-cs5014-18sp']:
		return 'instructional'
	elif row['partition'] in ['standard', 'parallel', 'largemem', 'dev', 'gpu', 'knl']:
		return 'research'
	else:
		return 'condo'


def get_pi(row):
	members = row['Users']
	pi = members.split("^")[-1].split(",")[0]  # re.search(r'\^(.*?)($|\,)', members).group(0)
	return pi


def merge_data(labels, usage_file, account_file, org_file, capacity_file, hours, groups=['Allocation']):
	capacity_df = pd.read_csv(capacity_file, delimiter='|')
	capacity_df['GPU devices'] = capacity_df.apply(lambda row: gpu_devices(row), axis=1)  # capacity_df['GRES'].str.extract(r'gpu\:.*?\:(\d+).*').fillna(0).astype(int)
	capacity_df = capacity_df.groupby(['PARTITION']).agg({"NODELIST": len, "CPUS": np.sum, "GPU devices": np.sum})
	capacity_df['Core hours'] = capacity_df['CPUS'] * hours
	capacity_df['GPU hours'] = capacity_df['GPU devices'] * hours
	cap_dict = capacity_df.to_dict('index')
	print(capacity_df)
	capacity_df.to_csv(f"{capacity_file[:-4]}-summary.csv")

	# labels = labels.split(',')
	# usage_df = pd.read_fwf(usage_file, widths=[11,51,11,11,11,11], names=labels) #, header=0, skiprows=7)
	usage_df = pd.read_csv(usage_file, delimiter="|")  # r"\s+", names=labels) #, header=0, skiprows=7)
	# print (usage_df.head())
	# new_cols = ['Total CPU hours', 'GPU devices', 'Total GPU hours', 'state', 'JobType', 'Utilization', 'PartitionType']
	usage_df['Total CPU hours'] = usage_df['cputimeraw'] / 3600
	usage_df['GPU devices'] = usage_df['alloctres'].str.extract(r'gres/gpu=(\d+)').fillna(0).astype(
		int)  # .apply(lambda row:get_gpu_devices(row), axis=1)
	# print (usage_df.head())
	usage_df['Total GPU hours'] = usage_df.apply(lambda row: calc_gpu_hours(row), axis=1)
	usage_df['state'] = usage_df.apply(lambda row: job_state(row), axis=1)
	usage_df['JobType'] = usage_df.apply(lambda row: job_type(row), axis=1)
	usage_df['Utilization'] = usage_df.apply(lambda row: utilization(row, cap_dict), axis=1)
	usage_df['PartitionType'] = usage_df.apply(lambda row: partition_type(row), axis=1)

	usage_df = usage_df.drop(columns=["cputimeraw", "alloccpus", "GPU devices"])
	if "Utilization" in usage_df:
		usage_df = usage_df.drop(columns=["Utilization"])

	org_groups = [g for g in groups if g in usage_df.columns.values]
	usage_df = usage_df.groupby(org_groups).sum().reset_index()
	print(usage_df.head())

	account_df = pd.read_csv(account_file, delimiter=r"\s+", header=0)
	org_df = pd.read_csv(org_file, delimiter=r"\s+", header=0, names=['Organization', 'School'])
	cols = account_df.columns.values
	cols[0] = "Allocation"
	account_df.columns = cols
	account_df['PI'] = account_df.apply(lambda row: get_pi(row), axis=1)
	print(account_df)

	accts_and_orgs = pd.merge(account_df, org_df, on='Organization', how='outer', suffixes=('_left', '_right'))
	print(accts_and_orgs)
	combined = pd.merge(usage_df, accts_and_orgs, on='Allocation', how='left', suffixes=('_left', '_right'))
	print(combined)
	return combined


def filter_by_school(df: pd.DataFrame, school: str, filepath=".", fname="rivanna-stats") -> None:
	path = os.path.join(filepath, school)
	os.makedirs(f"{path}", exist_ok=True)
	# year and date in output file : rivanna-stats-YEAR-DATE
	if school == "all" or "School" not in df.columns:
		df.to_csv(f"{path}/{fname}", index=False)
	else:
		df[df["School"] == school].to_csv(f"{path}/{fname}", index=False)


if __name__ == '__main__':
	parser = init_parser()
	args = parser.parse_args()
	school_filters = args.filter.split(",") # initialize filter variable
	if 'all' not in school_filters: school_filters.append('all')
	agroups = list(set(args.groups.replace('|', ',').split(',')))
	if 'Allocation' not in agroups:
		agroups.append('Allocation')
	print(f"agroups={agroups}")
	analysis = args.groups.split('|')
	hours = float(args.days) * 24
	df = merge_data(args.labels, args.usage, args.allocations, args.organizations, args.capacity, hours, groups=agroups)
	#df.to_csv(args.output, index=False)

	for school in school_filters:
		filter_by_school(df, school, filepath=args.path, fname=args.output)

	for r in analysis:
		print(''.join(["#"] * 80))
		groups = r.split(',') if args.groups != '' else ['Allocation']
		print(f'Analyzing by {r}, {groups}')
		for school in school_filters:
			sum_df = df.groupby(groups).sum().reset_index()  # does this need to be inside inner loop
			ftrunk, ext = os.path.splitext(args.output)
			fname = f"{ftrunk}-{''.join(groups)}-{school}{ext}"
			print(fname)
			#if "School" not in sum_df.columns:
			#	continue
			filter_by_school(sum_df, school, filepath=args.path, fname=fname)
			
			# These print statements are meaningless if repeated on the same unfiltered sum_df
			# print(sum_df)
			# print(sum_df.sum())
			# print("------------------------------------")
			# print(f"Total CPU Hours: {df['Total CPU hours'].sum():,.2f}")
			# print(f"Total GPU Device Hours: {df['Total GPU hours'].sum():,.2f}")
			
			groups = r.split(',') if args.groups != '' else ['User']
