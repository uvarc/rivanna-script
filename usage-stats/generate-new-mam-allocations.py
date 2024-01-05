#!/usr/bin/env python

import pandas as pd
import sys


def extract_pi(users_list: [str]):
	return next((user.strip("^") for user in users_list if "^" in user), None)


def create_pis_series(users_series: pd.Series) -> pd.Series:
	return pd.Series([extract_pi(users.split(",") if isinstance(users, str) else []) for users in users_series])


if __name__ == "__main__":
	try:
		year = sys.argv[1]
		month = sys.argv[2]
		output_path = sys.argv[3]
	except IndexError:
		print("Usage: python [script] YEAR MONTH OUTPUT_PATH")
		raise OSError
	allocation_accounts_df = pd.read_csv(f"{output_path}/allocationsaccounts.csv")
	combined_pis_df = pd.read_csv(f"{output_path}/Combined_allocationPIsFull.csv")
	allocations_year_month_df = pd.read_csv(f"{output_path}/allocations-{year}-{month}.csv")
	print(allocations_year_month_df.columns)
	allocation_accounts_df["PI"] = create_pis_series(allocation_accounts_df["Users"])
	merged_df = pd.merge(allocation_accounts_df, combined_pis_df, left_on='PI', right_on='UserID', how='left')
	merged_df = pd.merge(allocations_year_month_df, merged_df, on="Name", how="left")
	merged_df.to_csv(f"{output_path}/new-mam-allocations-{year}-{month}.csv")
