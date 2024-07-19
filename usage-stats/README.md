# Rivanna Script - Rivanna Utilization Statistics

Welcome to the Rivanna Script Repository, a collection of scripts designed to facilitate the generation of usage statistics, allocation reports, and user management on the Rivanna high-performance computing (HPC) environment. This README provides instructions on how to get started with these scripts, including cloning the repo, setting up the environment, and running the scripts for generating reports.

## Cloning the Repo

To clone the repository, use the following command in your terminal:

```bash
git clone https://github.com/galitz-matt/rivanna-script.git
```

## Setting the PATH

Before running the scripts, you need to ensure you are in the repository's script directory. 

```bash
cd /path/to/repo/rivanna-script/usage-stats/
```
Replace `path/to/repo` with the path where you have cloned the repository (do not include the "rivanna-script" portion of the path). 

## Running the Install Script

Before using the scripts, you need to run the `install.sh` script to set up the necessary environment. This script will create a Conda environment with all required dependencies.

Usage:

```bash
./install.sh path/to/dir-with-repo
```

Replace `path/to/repo` with the path where you have cloned the repository (do not include the "rivanna-script" portion of the path). The script will perform the following actions:

- Create a Conda environment using the `environment.yml` file.
- Set the execute permissions for all `.sh` and `.py` files in the repo.

Example:

```bash
./install.sh /home/user/dir_with_cloned_repo
```

## Activating the Conda Environment

After installation, you need to activate the Conda environment to use the scripts. This can be done with the following commands:

```bash
ml anaconda
source activate /path/to/repo/rivanna-script/usage-stats/rivanna-util-env
```

Replace `/path/to/repo` with the actual path to your cloned repository.

## Running the Scripts

The repository contains several scripts for generating reports and managing user allocations. Here is an example of how to run the `monthly-report.sh` script:

```bash
./monthly-report.sh 2024 03 31 "School:[DS]|Organization:[cab]|all" /path/to/output/dir
```

Arguments:
- `2024 03 31`: The date for the report in `year month days` format.
- `School:[DS]|Organization:[cab]|all`: Filtering options for the report. Replace or extend this argument according to your specific needs.
- `/project/arcs/rivanna-stats`: The output directory where the report will be saved.

Abbreviations:


Make sure to replace the arguments with values that match your requirements.

## Scheduling the Monthly Report Script with Scrontab
#### As of the time of publication (April 2, 2024) scrontab is only enabled on the derp cluster.
The Rivanna HPC system uses `scrontab`, a Slurm crontab tool, to schedule jobs to run at regular intervals. This section outlines how to schedule the `schedule-monthly-report.sh` script to automatically run at the beginning of each month to generate the previous month's report.

### Step 1: Prepare the Script
Configure your `scron.sh`. There are directions included within the script on what to change denoted by `TODO`.

### Step 2: Edit Your Scrontab File
To edit your scrontab entries, execute:
```bash
scrontab -e
```
This command opens your user-specific scrontab file in the default text editor set in your environment. (You can change your default editor with `export EDITOR=<path/to/editor_binary>`)

### Step 3: Add your Script to Scrontab
In the editor, add a new line to schedule your script. To run it at the beginning of each month, use the following crontab syntax:
```
0 0 1 * * /path/to/your/scron.sh
```

### Step 4: Save and Exit
After adding the entry, save your changes and exit the editor. Your script is now scheduled to run automatically.

### Step 5: Monitor Your Scheduled Jobs
You can view your scheduled scrontab jobs at any time by running:
```bash
scrontab -l
```

### Consult Documentation
The documentation for scrontab can be found here: https://docs.nersc.gov/jobs/workflow/scrontab/

---

Please ensure you have the necessary permissions to run these scripts and access the specified directories and data.
