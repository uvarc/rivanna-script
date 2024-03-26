#!/bin/bash

set -eo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: `basename $0` path/to/repo"
    exit 1
fi

DIR="$1"
PROJECT_PATH="$DIR/rivanna-script/usage-stats"
PREFIX="$PROJECT_PATH/rivanna-util-env"
YML="$PROJECT_PATH/environment.yml"

module load anaconda || { echo "Failed to load anaconda module"; exit 1 }
conda env create -f "$YML" --prefix "$PREFIX" || { echo "Failed to create conda environment"; exit 1; }
module unload anaconda

find "$PROJECT_PATH" -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod 750 {} \;

echo "Setup complete. Please activate the conda environment with 'ml anaconda && source activate $PREFIX' before use." 
