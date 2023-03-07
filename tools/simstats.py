#!/usr/bin/env python2

import sys, os, json, sniper_lib

WORKLOADS_DIRECTORY = "/home/vivoape/master_project/sniper_traces/spec_cpu2017_reference_w0_d1B/"

METRICS = (
    'performance_model.cycle_count',
    'rob_timer.numContentionBlocks',
    'rob_timer.numContentionCycles',
)

def get_results(results_dir, metrics=None):
    res = sniper_lib.get_results(resultsdir=results_dir)
    results = res['results']

    if metrics:
        filtered_results = {}
        for metric in metrics:
            if metric in results:
                filtered_results[metric] = results[metric]
        return filtered_results
    else:
        return results

def get_workloads_results(workloads_dir, metrics):
    all_results = {}
    workload_names = os.listdir(workloads_dir)
    for wl_name in workload_names:
        all_results[wl_name] = get_results(workloads_dir+wl_name, metrics)

    return all_results

args = sys.argv

if len(args) == 1:
    results = get_workloads_results(WORKLOADS_DIRECTORY, METRICS)
elif len(args) == 2:
    results = get_results(args[1])
else:
    results = get_results(args[1], args[2:])

print json.dumps(results, indent=4)

