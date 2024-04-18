if [ "$#" -ne 2 ]; then
    echo "Usage: `basename $0` YYYY MM"
    exit 1
fi

YEAR=$1
MONTH=$2

echo "removing temp files..."
rm activeusers-${YEAR}-${MONTH}.csv \
   activeusers-UIDs-${YEAR}-${MONTH}.txt \
   allocationPIsFull.csv \
   allocationPIs.txt \
   allocations-${YEAR}-${MONTH}.csv \
   allocationsaccounts.csv \
   newUIDs-${YEAR}-${MONTH}.txt \
   newusers-${YEAR}-${MONTH}.csv
echo "files removed successfully"
