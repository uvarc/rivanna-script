#!/bin/bash

if [ "$#" -ne 6 ]; then
    echo "Usage: `basename $0` YYYY-MM-DDThh:mm:ss YYYY-MM-DDThh:mm:ss outputfile days-in-period filter outputpath"
    exit 1
fi

today=$(date +%Y-%m-%d)

START=$1
END=$2
OUT_FILE=$3
DAYS=$4
FILTER=$5
OUTPUTPATH="$6"
mkdir -p $OUTPUTPATH

YYYYMM=`echo $START | cut -c1-7`
STATES="CANCELLED,COMPLETED,FAILED,NODE_FAIL,PREEMPTED,TIMEOUT,OUT_OF_MEMORY"
#CORE_USAGE_FILE=${OUTPUTPATH}/rivanna-corehours-${START}-${END}.csv
CAPACITY_FILE=${OUTPUTPATH}/rivanna-capacity-${START}-${END}.csv
ALLOC_FILE=${OUTPUTPATH}/rivanna-allocations-$today.txt
ORG_FILE=${OUTPUTPATH}/rivanna-organizations-$today.txt


COLUMNS="user,account%50,jobid%30,cputimeraw,alloctres%75,alloccpus,partition,planned,state,plannedcpuraw,reqcpus,submit,start,end"
LABELS="${COLUMNS/"account%50"/Allocation}" 
LABELS="${LABELS/"jobid%30"/jobid}"
LABELS="${LABELS/"planned"/reserved}"
LABELS="${LABELS/"plannedcpuraw"/resvcpuraw}"
LABELS="${LABELS/"alloctres%75"/alloctres}"

COLUMNS2="jobname%75"
LABELS2="${COLUMNS2/"jobname%75"/JobName}"

COLUMNS3="constraint%50"
LABELS3="${COLUMNS3/"constraint%50"/constraint}"

CORE_USAGE_FILE=${OUTPUTPATH}/rivanna-corehours-${START}-${END}.csv
echo "$LABELS" | tr \, \| > $CORE_USAGE_FILE
CORE_USAGE_FILE2=${OUTPUTPATH}/rivanna-corehours2-${START}-${END}.csv
echo "$LABELS2" | tr \, \| > $CORE_USAGE_FILE2
CORE_USAGE_FILE3=${OUTPUTPATH}/rivanna-corehours3-${START}-${END}.csv
echo "$LABELS3" | tr \, \| > $CORE_USAGE_FILE3

TZ=UTC sacct -P -n -a -X -S ${START} -E ${END} -s ${STATES} --format=${COLUMNS} | awk -F'|' 'BEGIN {OFS="|"} {gsub(/\,/, ";", $3); gsub(/\,/, ";", $5); gsub(/\,/, ";", $7); print $0}' >> $CORE_USAGE_FILE
TZ=UTC sacct -P -n -a -X -S ${START} -E ${END} -s ${STATES} --format=${COLUMNS2} | awk -F'|' 'BEGIN {OFS="|"} {print "\"" $0 "\""}' >> $CORE_USAGE_FILE2
TZ=UTC sacct -P -n -a -X -S ${START} -E ${END} -s ${STATES} --format=${COLUMNS3} | awk -F'|' 'BEGIN {OFS="|"} {print "\"" $0 "\""}' >> $CORE_USAGE_FILE3

# sed -i 's/chr.*slurm/chr slurm/g' $CORE_USAGE_FILE

sinfo -N --format="%R|%N|%T|%c|%G" > $CAPACITY_FILE

sudo /opt/mam/current/bin/mam-list-accounts > $ALLOC_FILE
/opt/mam/current/bin/mam-list-organizations > $ORG_FILE
python refactor-orgfile.py $ORG_FILE 

sed -i 's/Health_Volunteer Volunteer sponsored/Health_Volunteer_Volunteer_sponsored/g' $ALLOC_FILE
sed -i 's/Health_Volunteer Volunteer sponsored/Health_Volunteer_Volunteer_sponsored/g' $ORG_FILE

python core-usage-summary.py -d $DAYS -c $CAPACITY_FILE -u $CORE_USAGE_FILE -u2 $CORE_USAGE_FILE2 -u3 $CORE_USAGE_FILE3 -x $ORG_FILE -a $ALLOC_FILE -l "$LABELS" -p "${OUTPUTPATH}/{FILTER}/${YYYYMM}" -o $OUT_FILE -g "PI,School|Allocation,Description,PI,School|Allocation,Description,PI,School,partition|School,Organization|user,School|Allocation,user,PI,School,Organization|user,Allocation,PI,School,Organization|School|School,JobType|School,partition|School,partition,JobType" -f "${FILTER}"