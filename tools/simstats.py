#from sniper_stats_sqlite import SniperStatsSqlite
import sniper_lib
import subprocess

'''
object_name = 'rob_timer'

stats = SniperStatsSqlite()
metric_names = stats.read_metricnames()
end_snapshot = stats.read_snapshot('stop')

metrics_to_get = (('rob_timer', 'numContentionBlocks'), ('rob_timer', 'numContentionCycles'))
metrics = []

for nameid, metric_name in metric_names.items():
    if metric_name in metrics_to_get:
        value = end_snapshot[nameid][0] if (nameid in end_snapshot) else None
        metrics.append((metric_name, value))        

print(metrics)

'''

#trace_file = '../sniper_traces/spec_cpu2017_reference_w0_d1B/gcc_r_1/gcc_r_1_trace.sift'
#subprocess.call(f'./run-sniper -v -n 1 -c rakesh -c robOoO_000_NoQ_256ROB --traces {trace_file}', shell=True)

res = sniper_lib.get_results(resultsdir='.')

results = res['results']
config = res['config']
ncores = int(config['general/total_cores'])

if 'barrier.global_time_begin' in results:
    time0_begin = results['barrier.global_time_begin']
    time0_end = results['barrier.global_time_end']

if 'barrier.global_time' in results:
    time0 = results['barrier.global_time'][0]
else:
    time0 = time0_begin - time0_end

if sum(results['performance_model.instruction_count']) == 0:
    # core.instructions is less exact, but in cache-only mode it's all there is
    results['performance_model.instruction_count'] = results['core.instructions']

results['performance_model.elapsed_time_fixed'] = [
    time0
    for c in range(ncores)
]

results['performance_model.cycle_count_fixed'] = [
    results['performance_model.elapsed_time_fixed'][c] * results['fs_to_cycles_cores'][c]
    for c in range(ncores)
]

print()
print('Cycles:', results['performance_model.cycle_count_fixed'])
print('Cycles w/ contention:', results['rob_timer.numContentionCycles'])
print('Contention blocks:', results['rob_timer.numContentionBlocks'])
print()
print('Percentage of cycles with contention:', 100*(float(results['rob_timer.numContentionCycles'][0])/results['performance_model.cycle_count_fixed'][0]))
print('Avg blocks per cont. cycle:', float(results['rob_timer.numContentionBlocks'][0])/results['rob_timer.numContentionCycles'][0])
print()
