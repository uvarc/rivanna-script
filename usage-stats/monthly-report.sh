#!/bin/bash

# update condition to account for FILTER arg
if [ "$#" -ne 5 ]; then
    echo "Usage: `basename $0` YYYY MM DAYS FILTER OUTPUTPATH"
    exit 1
fi

SYEAR=$1
SMONTH=$2
DAYS=$3
FILTER=$4 # new assignment
OUTPUTPATH=$5

SDAY=01
FIRSTDAYMONTH=${SYEAR}-${SMONTH}-${SDAY}
FIRSTNEXTMONTH=$(date -d "${SYEAR}${SMONTH}${SDAY}+1 month" +%Y-%m-%d)
LASTDAYMONTH=$(date -d "${FIRSTNEXTMONTH}-1 day" +%Y-%m-%d)
echo "Reporting $FIRSTDAYMONTH through $LASTDAYMONTH"
echo "Writing to $OUTPUTPATH"

module purge
module load anaconda/2019.10-py2.7
newusers-report.sh ${SYEAR} ${SMONTH} newusers-${SYEAR}-${SMONTH}.csv

get-allocation-data.sh ${SYEAR} ${SMONTH}
#su-transactions.py -f allocations.html -s ${SYEAR}-${SMONTH}-${SDAY} -e ${FIRSTNEXTMONTH} -o newallocations-${SYEAR}-${SMONTH}.csv
#su-transactions.py -f allocations.html -s ${SYEAR}-${SMONTH}-${SDAY} -e ${FIRSTNEXTMONTH} -o newallocations-${SYEAR}-${SMONTH}-schooltype.csv -g "School,Type"
#su-transactions.py -f allocations.html -s ${SYEAR}-${SMONTH}-${SDAY} -e ${FIRSTNEXTMONTH} -o newallocations-${SYEAR}-${SMONTH}-typeschool.csv -g "Type,School"

module load anaconda
core-usage-report.sh ${FIRSTDAYMONTH}T00:00:00 ${LASTDAYMONTH}T23:59:59 corehours-${SYEAR}-${SMONTH}.csv $DAYS $FILTER $OUTPUTPATH
# added $FILTER argument 

# filter cpurawtime>0 (5th column in corehours-${SYEAR}-${SMONTH}.csv, and get uids
#awk -F, '{ if ($2 > 0) print $1 }' all/corehours-${SYEAR}-${SMONTH}-userSchool-all.csv | head
awk -F, '{ if ($2 > 0) print $1 }' all/corehours-${SYEAR}-${SMONTH}-userSchool-all.csv | sort -u > activeusers-UIDs-${SYEAR}-${SMONTH}.txt
ldapreport.sh activeusers-UIDs-${SYEAR}-${SMONTH}.txt > activeusers-${SYEAR}-${SMONTH}.csv
module load anaconda/2019.10-py2.7
mergeusers.py activeusers-${SYEAR}-${SMONTH}.csv
