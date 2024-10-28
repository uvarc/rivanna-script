#!/usr/bin/env python

import pandas as pd
import sys
from typing import List, Optional


def extract_pi(users_list: List[str]) -> Optional[str]:
    """Extracts a PI identifier from a list of users."""
    return next((user.strip("^") for user in users_list if "^" in user), None)


def create_pis_series(users_series: pd.Series) -> pd.Series:
    """Creates a Pandas Series of PI identifiers from a series of user strings."""
    return pd.Series([extract_pi(users.split(",") if isinstance(users, str) else []) for users in users_series])


if __name__ == "__main__":
    try:
        year: str = sys.argv[1]
        month: str = sys.argv[2]
        output_path: str = sys.argv[3]
    except IndexError:
        print("Usage: python generate-new-mam-allocations.py YEAR MONTH OUTPUT_PATH")
        sys.exit(1)

    # Reading data from CSV files
    allocation_accounts_df: pd.DataFrame = pd.read_csv(f"{output_path}/allocationsaccounts.csv")
    combined_pis_df: pd.DataFrame = pd.read_csv(f"{output_path}/Combined_allocationPIsFull.csv")
    allocations_year_month_df: pd.DataFrame = pd.read_csv(f"{output_path}/allocations-{year}-{month}.csv")

    # Processing data to merge PI information
    allocation_accounts_df["PI"] = create_pis_series(allocation_accounts_df["Users"])
    merged_df: pd.DataFrame = pd.merge(allocation_accounts_df, combined_pis_df, left_on='PI', right_on='UserID', how='left')
    merged_df = pd.merge(allocations_year_month_df, merged_df, on="Name", how="left")

    # Saving the processed data to a new CSV file
    merged_df.to_csv(f"{output_path}/new-mam-allocations-{year}-{month}.csv")
