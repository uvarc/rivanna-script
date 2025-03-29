#!/bin/bash

if [ "$#" -ne 6 ]; then
    echo "Usage: `basename $0` YYYY MM DAYS FILTER OUTPUTPATH DATAPATH"
    exit 1
fi

SCRIPT_PATH="/home/ykk6rh/rivanna-script/usage-stats"

# monthly-report params
SYEAR=$1
echo $SYEAR
SMONTH=$2
echo $SMONTH
DAYS=$3
echo $DAYS
FILTER=$4
OUTPUTPATH=$5
DATAPATH=$6

SDAY=01
FIRSTDAYMONTH=${SYEAR}-${SMONTH}-${SDAY}
echo $FIRSTDAYMONTH
FIRSTNEXTMONTH=$(date -d "${SYEAR}${SMONTH}${SDAY}+1 month" +%Y-%m-%d)
LASTDAYMONTH=$(date -d "${FIRSTNEXTMONTH}-1 day" +%Y-%m-%d)

# core-usage-report params
START="${FIRSTDAYMONTH}T00:00:00"
END="${LASTDAYMONTH}T23:59:59"
OUT_FILE="corehours-${SYEAR}-${SMONTH}.csv"
DAYS=${DAYS}
FILTER=${FILTER}
OUTPUTPATH=${OUTPUTPATH}

# core-usage-summary params
CORE_USAGE_FILE=${DATAPATH}/rivanna-corehours-${START}-${END}.csv
CAPACITY_FILE=${DATAPATH}/rivanna-capacity-${START}-${END}.csv
CORE_USAGE_FILE2=${DATAPATH}/rivanna-corehours2-${START}-${END}.csv
CORE_USAGE_FILE3=${DATAPATH}/rivanna-corehours3-${START}-${END}.csv
# Update with specific file names
ALLOC_FILE=${DATAPATH}/rivanna-allocations-2024-03-15.txt
ORG_FILE=${DATAPATH}/rivanna-organizations-2024-03-15.txt
YYYYMM=`echo $START | cut -c1-7`

LABELS="user,account,jobid,cputimeraw,alloctres,alloccpus,partition,reserved,state,resvcpuraw,reqcpus,submit,start,end,jobname,constraint"

bash core-usage-report.sh ${FIRSTDAYMONTH}T00:00:00 ${LASTDAYMONTH}T23:59:59 corehours-${SYEAR}-${SMONTH}.csv $DAYS "${FILTER}" $OUTPUTPATH

#${SCRIPT_PATH}/core-usage-summary.py -d $DAYS -c $CAPACITY_FILE -u $CORE_USAGE_FILE -u2 $CORE_USAGE_FILE2 -u3 $CORE_USAGE_FILE3 -x $ORG_FILE -a $ALLOC_FILE -l "$LABELS" -p "${OUTPUTPATH}/{FILTER}/${YYYYMM}" -o $OUT_FILE -g "PI,School|Allocation,Description,PI,School|Allocation,Description,PI,School,partition|School,Organization|user,School|Allocation,user,PI,School,Organization|user,Allocation,PI,School,Organization|School|School,JobType|School,partition|School,partition,JobType" -f "${FILTER}"
