YEAR=$1
MONTH=$2
OUTPUT=$3

echo "removing temp files..."

declare -a files_to_remove=(
    "${OUTPUT}/activeusers-${YEAR}-${MONTH}.csv"
    "${OUTPUT}/activeusers-UIDs-${YEAR}-${MONTH}.txt"
    "${OUTPUT}/allocationPIsFull.csv"
    "${OUTPUT}/allocationPIs.txt"
    "${OUTPUT}/allocations-${YEAR}-${MONTH}.csv"
    "${OUTPUT}/allocationsaccounts.csv"
    "${OUTPUT}/newUIDs-${YEAR}-${MONTH}.txt"
    "${OUTPUT}/newusers-${YEAR}-${MONTH}.csv"
)

for file in "${files_to_remove[@]}"; do
    if [ -f "$file" ]; then  # Check if file exists
        rm "$file"
        echo "Removed $file"
    else
        echo "File not found: $file"
    fi
done

echo "files removed successfully"
