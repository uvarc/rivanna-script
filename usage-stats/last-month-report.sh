#!/bin/bash

# Configured to report utilization data of prior month
year=$(date --date="$(date +%Y-%m-15) -1 month" +%Y)
month=$(date --date="$(date +%Y-%m-15) -1 month" +%m)
last_day=$(date -d "$year-$month-01 +1 month -1 day" +%d)

filter="School:[DS]|School:[EN]|School:[MD]|School:[ED]|School:[AS]|School:[MC]|School:[IT]|School:[DA]|School:[BA]|School:[PV]|School:[AR]|School:[NU]|School:[LW]|School:[CP]|Organization:[cab]|Organization:[bii]|all" 
output_dir="/project/arcs/rivanna-stats/" 
conda_env="/project/arcs/rivanna-util/rivanna-script/usage-stats/rivanna-util-env" 
SCRIPT="/project/arcs/rivanna-util/rivanna-script/usage-stats/monthly-report.sh" 

ml miniforge
source activate $conda_env
$SCRIPT $year $month $last_day $filter $output_dir
conda deactivate
module unload miniforge
