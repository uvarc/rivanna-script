if  [ "$#" -ne 2 ]; then
  echo "Usage: `basename $0` YEAR MONTH"
  exit 1
fi

YEAR=$1
MONTH=$2

echo "2359,Name,0,,Account=natashaironside,76358.562,0.000,100000.000,100000.000,2340:76358.5617:2023-10-01:2024-10-01,,,renewal_2023-10-01-19:29:40,2023-10-01 19:29:40,2023-10-01 19:29:40,False,56651014,358186893" > allocations-${YEAR}-${MONTH}.csv
sudo /opt/mam/current/bin/mam-list-funds --full --format csv|grep _${YEAR}-${MONTH} >> allocations-${YEAR}-${MONTH}.csv

sudo /opt/mam/current/bin/mam-list-accounts --full --format csv >> allocationsaccounts.csv

awk -F'^' '{print $2}' allocationsaccounts.csv | awk -F'[,"]' '{print $1}' > allocationPIs.txt
./ldapreport.sh allocationPIs.txt > allocationPIsFull.csv
ml anaconda/2019.10-py2.7
python mergeusers.py allocationPIsFull.csv
python generate-new-mam-allocations.py ${YEAR} ${MONTH}

