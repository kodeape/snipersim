#!/bin/bash

# Define the directory containing the workloads
DIRECTORY=/cluster/home/sarargh/sniper_traces/spec_cpu2017_reference_w0_d1B

# Get the list of subfolders
SUBFOLDERS=$(find $DIRECTORY/* -maxdepth 0 -type d)

# Loop through each subfolder
for folder in $SUBFOLDERS; do
  # Get the job name
  job_name=$(basename $folder)

  # Run the slurm script with the job name, max time, and command
  ./slurm-submit.sh $job_name 02:00:00 "./run-sniper -c rakesh.cfg -c robOoO_000_NoQ_256ROB.cfg --traces=$DIRECTORY/$job_name/${job_name}_trace.sift"

done
