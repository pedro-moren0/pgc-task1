import os
import subprocess

from paths import hotgp_path

population_range = list(range(100, 501, 50))
evaluation_range = list(range(10000, 100001, 5000))
benchmarks = ['compare-string-lengths', 'count-odds',
              'digits', 'double-letters', 'even-squares']
metrics = ['totalEvals', 'fitness', 'height', 'nodeCount', 'accuracy']


def runAllBenchmarks() -> None:
    os.chdir(hotgp_path)
    for bench in benchmarks:
        for pop in population_range:
            for eval in evaluation_range:
                for seed in range(0, 11):
                    subprocess.run(
                        ['stack', 'run', 'itask1', str(
                            pop), str(eval), str(seed), bench]
                    )


def runBenchmark(bench: str) -> None:
    os.chdir(hotgp_path)
    for pop in population_range:
        for eval in evaluation_range:
            for seed in range(0, 11):
                subprocess.run(
                    ['stack', 'run', 'itask1', str(
                        pop), str(eval), str(seed), bench]
                )
