#!/bin/bash

echo "NOTE: run script at root level of cloned repository"

if [ "$#" -ne 1 ]; then
    echo "Usage: `basename $0` path/to/new-conda-env"
    exit 1
fi

DIR=$1
ENV_NAME="rivanna-util-env"

ml anaconda
conda env create -f usage-stats/environment.yml -n $ENV_NAME # add conda env prefix w/ dir var
module unload anaconda
find $DIR -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod 750 {} \;

#LINE="export PATH=$DIR/rivanna-script/usage-stats/:$PATH"
#FILE="$HOME/.bashrc"
#grep -qxF "$LINE" "$FILE" || echo "$LINE" >> "$FILE"

echo "Setup complete. Please activate the conda environment with 'ml anaconda && source activate $DIR/$ENV_NAME' before use." # double check how conda prefixes work
