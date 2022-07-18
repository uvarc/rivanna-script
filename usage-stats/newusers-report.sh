#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: `basename $0` YYYY MM outputfile"
    exit 1
fi

date=$(date '+%Y-%m-%d')

YEAR=$1
MONTH=$2
OUTPUTFILE=$3

FIRSTDAY=$(date -d "$YEAR/$MONTH/1" "+%Y-%m-%d")
LASTDAY=$(date -d "$FIRSTDAY + 1 month " "+%Y-%m-%d")
#LASTDAY=$(date -d "$FIRSTDAY + 1 year " "+%Y-%m-%d")
echo "New users in $YEAR/$MONTH"
echo $FIRSTDAY - $LASTDAY

SUFFIX=${YEAR}-${MONTH}
USERIDS=newUIDs-${SUFFIX}.txt
echo Getting new accounts
mam-list-users --full -A --format=csv | awk -F"," -v FIRST=$FIRSTDAY -v LAST=$LASTDAY '{ if ($2=="True" && $8>=FIRST && $8<LAST) { print $1 } }' > $USERIDS
echo New UIDs saved in $USERIDS

echo Searching LDAP
echo Done.
echo ---------------------------------

ldapreport.sh $USERIDS > $OUTPUTFILE

mergeusers.py $OUTPUTFILE
#sacctmgr list associations format=Account%30,User | uniq > $USERLIST
