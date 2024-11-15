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
ENTRY="core-usage-summary.py"
CORE_USAGE_FILE=${DATAPATH}/rivanna-corehours-${START}-${END}.csv
CAPACITY_FILE=${DATAPATH}/rivanna-capacity-${START}-${END}.csv
ALLOC_FILE=${DATAPATH}/rivanna-allocations-2024-07-10.txt
ORG_FILE=${DATAPATH}/rivanna-organizations-2024-07-10.txt
YYYYMM=`echo $START | cut -c1-7`
COLUMNS="user,account%50,jobid,cputimeraw,alloctres,alloccpus,partition,planned,state,plannedcpuraw,reqcpus,submit,start,end,jobname%30"
LABELS="${COLUMNS/"account%50"/Allocation}"
LABELS="${LABELS/"jobname%30"/JobName}"
LABELS="${LABELS/"planned"/reserved}"
LABELS="${LABELS/"plannedcpuraw"/resvcpuraw}"

core-usage-report.sh ${FIRSTDAYMONTH}T00:00:00 ${LASTDAYMONTH}T23:59:59 corehours-${SYEAR}-${SMONTH}.csv $DAYS "${FILTER}" $OUTPUTPATH

${SCRIPT_PATH}/core-usage-summary.py -d $DAYS -c $CAPACITY_FILE -u $CORE_USAGE_FILE -x $ORG_FILE -a $ALLOC_FILE -l "$LABELS" -p "${OUTPUTPATH}/{FILTER}/${YYYYMM}" -o $OUT_FILE -g "PI,School|Allocation,Description,PI,School|Allocation,Description,PI,School,partition|School,Organization|user,School|Allocation,user,PI,School,Organization|user,Allocation,PI,School,Organization|School|School,JobType|School,partition|School,partition,JobType" -f "${FILTER}"
