#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Sep 13 21:32:40 2020

Refactored on [Refactoring Date]

@author: khs3z
"""

import pandas as pd
import argparse
from pathlib import Path
from typing import Dict, List


def init_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge user data with school affiliations.")
    parser.add_argument('uidfile', type=str, help='Path to the input CSV file containing user IDs.')
    parser.add_argument('output_path', type=str, help='Path to the output directory.')
    return parser


def lookup_school(row: pd.Series, schools: Dict[str, List[str]]) -> str:
    dept_lower = row['Dept'].lower()
    affil_lower = row['Affiliation'].lower()

    for school, keywords in schools.items():
        if any(keyword in dept_lower for keyword in keywords) or any(keyword in affil_lower for keyword in keywords):
            return school
    return 'OTHER'


def main(uidfile_path: str, output_path_str: str) -> None:
    output_path = Path(output_path_str)
    uidfile = Path(uidfile_path)

    schools = {
        'AS': ['e0:as', 's0:as', 's1:as', 's3:as', 'arts', 'global public health', 'english', 'economics', 'psychology',
               'environmental', 'politics', 'biology', 'chemistry'],
        'EN': ['e0:en', 's0:en', 's1:en', 's2:en', 'engineer', 'systems', 'computer', 'materials'],
        'MD': ['e0:interns and  resident', 'e0:md', 'som', 'global health', 'cphg', 'physical therapy',
               'public health genomics', 'public health science', 'public health services', 'pharma', 'md-micr',
               'biomed', 'infect', 'neuroscience', 'medicine', 'cardiovascular', 'cell bio', 'pediatrics', 'immunology',
               'microbio'],
        'DS': ['data', 'dsi', 'sds', 'e0:ds'],
        'DA': ['da:', 'e0:da', 'darden', 'business'],
        'ED': ['ed:', 'education', 'teaching'],
        'MC': ['e0:mc', 'mcintire', 'commerce', 'mc-'],
        'BA': ['e0:cu-leadshp', 'batten'],
        'RC': ['e0:it-research computing', 'research-computing'],
        'BI': ['e0:pv-bii', 's0:pv-bii', 'biocomplexity'],
        'PV': ['pv-'],
        'CP': ['school for continuing and professional studies'],
        'AR': ['architecture'],
        'NR': ['nursing']
    }

    uid_df = pd.read_csv(uidfile, names=["UserID", "Lastname", "Firstname", "Affiliation", "Status"])
    uid_df['School'] = uid_df.apply(lookup_school, schools=schools, axis=1)

    output_file = output_path / f"Combined_{uidfile.name}"
    uid_df.to_csv(output_file, index=False)
    print(uid_df)
    print('-------------------------------------------')


if __name__ == "__main__":
    parser = init_arg_parser()
    args = parser.parse_args()
    main(args.uidfile, args.output_path)
