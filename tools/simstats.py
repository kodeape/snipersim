#!/usr/bin/env python2

import sys, os, json, sniper_lib

DEFAULT_RESULTS_DIRECTORY = "/cluster/home/sarargh/sniper/results"

DEFAULT_METRICS = None
#METRICS = (
#    'performance_model.cycle_count',
#    'rob_timer.numContentionBlocks',
#    'rob_timer.numContentionCycles',
#)

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

def get_results_recursive(dir, metrics=None):
    try:
        return get_results(dir, metrics)
    except:
        results = {}
        subdirs = os.listdir(dir)
        for subdir in subdirs:
            subdir_path = os.path.join(dir, subdir)
            if os.path.isdir(subdir_path):
                subresults = get_results_recursive(subdir_path, metrics)
                if subresults:
                    results[subdir] = subresults
        return results

if __name__ == '__main__':

    args = sys.argv

    if len(args) == 1:
        results = get_results_recursive(DEFAULT_RESULTS_DIRECTORY, DEFAULT_METRICS)
    elif len(args) == 2:
        results = get_results_recursive(args[1], DEFAULT_METRICS)
    else:
        results = get_results_recursive(args[1], args[2:])

    print json.dumps(results, indent=4)
