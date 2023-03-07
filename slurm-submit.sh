#!/bin/bash

# Print usage message
usage() {
  echo "Usage: $0 JOB_NAME MAX_TIME JOB_COMMAND"
  echo "JOB_NAME: the name of the job"
  echo "MAX_TIME: the maximum time the job is allowed to run (format: HH:MM:SS)"
  echo "JOB_COMMAND: the command to run for the job (enclose in quotes if it contains spaces)"
  exit 1
}

# Check for correct number of arguments
if [ $# -ne 3 ]; then
  usage
fi

# Check that max time is in correct format
if ! [[ $2 =~ ^[0-9]{2}:[0-9]{2}:[0-9]{2}$ ]]; then
  echo "Error: MAX_TIME must be in the format HH:MM:SS"
  usage
fi

# Variables for the slurm script
PARTITION=CPUQ
ACCOUNT=share-ie-idi
NODES=1
NTASKS_PER_NODE=1
CPUS_PER_TASK=1
MEMORY=4G

# Print job information
echo "Job information:"
echo "-----------------"
echo "Job command          : $3"
echo "Max time             : $2"
echo "Job name             : $1"
echo "Partition            : $PARTITION"
echo "Account              : $ACCOUNT"
echo "Nodes                : $NODES"
echo "Tasks per node       : $NTASKS_PER_NODE"
echo "Cores per task       : $CPUS_PER_TASK"
echo "Memory               : $MEMORY"
echo "-----------------"

# Submit job to SLURM
sbatch --output=$1.out <<EOF
#!/bin/sh
#SBATCH --partition=$PARTITION
#SBATCH --account=$ACCOUNT
#SBATCH --job-name=$1
#SBATCH --nodes=$NODES
#SBATCH --ntasks-per-node=$NTASKS_PER_NODE
#SBATCH --cpus-per-task=$CPUS_PER_TASK
#SBATCH --mem=$MEMORY
#SBATCH --time=$2

# Run job command
$3
EOF
