#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: `basename $0` YYYY-MM-DDThh:mm:ss YYYY-MM-DDThh:mm:ss outputfile"
    exit 1
fi

today=$(date +%Y-%m-%d)

START=$1
END=$2
OUT_FILE=$3
CORE_USAGE_FILE=rivanna-corehours-${START}-${END}.csv
ALLOC_FILE=rivanna-allocations-$today.txt
ORG_FILE=rivanna-organizations-$today.txt

#if [ -f $CORE_USAGE_FILE ]; then
#   rm $CORE_USAGE_FILE
#fi
#accs=( $(sacctmgr list account Format=Account%50 -n ))
#for acc in ${accs[@]}; do
#    echo Processing ${acc}    
#    sacct -n -A ${acc} -a -S ${START} -E ${END} --format=user,cputimeraw,account%50| awk '$3'|awk '{ counts[$3]++; totals[$3] += $2;} END { for (x in counts) { print x","totals[x]/3600; }}' >> $CORE_USAGE_FILE 
#    sleep 1
#done

# get raw data
sacct -n -a -X -S ${START} -E ${END} --format=account%50,cputimeraw |awk '{ counts[$1]++; totals[$1] += $2;} END { for (x in counts) { print x","totals[x]/3600; }}' > $CORE_USAGE_FILE
sudo /opt/mam/current/bin/mam-list-accounts > $ALLOC_FILE
/opt/mam/current/bin/mam-list-organizations > $ORG_FILE 

# create summary
python core-usage-summary.py -c $CORE_USAGE_FILE -x $ORG_FILE -a $ALLOC_FILE -o $OUT_FILE

# clean up
rm $CORE_USAGE_FILE 
rm $ORG_FILE
rm $ALLOC_FILE
