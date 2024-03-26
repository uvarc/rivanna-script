#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: `basename $0` path/to/repo"
    exit 1
fi

DIR=$1
PROJECT_PATH=$DIR/rivanna-script/usage-stats
PREFIX=$PROJECT_PATH/rivanna-util-env
YML=$PROJECT_PATH/environment.yml

module load anaconda
conda env create -f $YML --prefix $PREFIX 
module unload anaconda
find $PROJECT_PATH -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod 750 {} \;

echo "Setup complete. Please activate the conda environment with 'ml anaconda && source activate $PROJECT_PATH/$ENV_NAME' before use." 
