#!/bin/bash

# Define the directory containing the workloads
DIRECTORY=/cluster/home/sarargh/sniper_traces/spec_cpu2017_reference_w0_d1B

# Get the list of subfolders
SUBFOLDERS=$(find "$DIRECTORY"/* -maxdepth 0 -type d)

RESDIR="./results"
NRUNS=5

# Get configs
if [ -d "$1" ]; then
  CONFIGS=$(find "$1"/* -name "*.cfg" -maxdepth 0 -type f)
else
  CONFIGS="$@"
fi

# Clear/make the results directory
if [ -d "$RESDIR" ]; then
  rm -r "$RESDIR"
fi
mkdir "$RESDIR"

for cfg in $CONFIGS; do

  cfg_name=$(basename "${cfg%.*}")
  mkdir "$RESDIR/$cfg_name"

  for i in `seq 1 $NRUNS`; do
    # Make result subdirectory for this run
    mkdir "$RESDIR/$cfg_name/run$i"

    # Loop through each subfolder
    for folder in $SUBFOLDERS; do
      # Get the job name
      job_name=$(basename "$folder")

      # Make the job result directory
      job_res_dir="$RESDIR/$cfg_name/run$i/$job_name"
      mkdir "$job_res_dir"

      # Run the slurm script with the job name, max time, and command
      ./slurm-submit.sh ${cfg_name}_run${i}_${job_name} 02:30:00 "./run-sniper -c rakesh.cfg -c robOoO_000_NoQ_256ROB.cfg -c $cfg -d $job_res_dir --traces=$DIRECTORY/$job_name/${job_name}_trace.sift"
    done
  done
done