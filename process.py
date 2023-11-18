import os
import json
import re
from statistics import mean
from ast import literal_eval

import pandas as pd
import matplotlib.pyplot as plt

from paths import hotgp_output_path, process_output_target
from run import *

file_name_regex = r'^p(\d{3})_e(\d{5,6})_s(\d{1,2})_(.+)\.result\.json$'


def peek(x):
    print(x)
    print(type(x))
    return x


def process() -> None:
    fileList = list(filter(lambda x: x.endswith(
        '.result.json'), os.listdir(hotgp_output_path)))

    results_per_benchmark = {
        b: {
            m: pd.DataFrame(
                data=[([] for _ in evaluation_range)
                      for _ in population_range],
                index=population_range,
                columns=evaluation_range
            )
            for m in metrics
        }
        for b in benchmarks
    }

    for f_name in fileList:
        pop_size, eval_num, _, benchmark = re.search(
            file_name_regex, f_name).groups()
        if benchmark not in benchmarks:
            continue
        with open(hotgp_output_path + '/' + f_name) as file:
            best_data = json.load(file)
            for metric, value in best_data.items():
                if metric in metrics:
                    results_per_benchmark[benchmark][metric].at[int(pop_size), int(eval_num)].append(
                        value)
    avg_results_compare_string_lengths = {
        m: df.map(lambda xs: mean(map(lambda x: float(x), xs))) for m, df in results_per_benchmark['compare-string-lengths'].items()
    }
    # results_per_benchmark['double-letters']['totalEvals'].to_csv(
    #     os.path.join('./output/', 'totalEvals_double-letters.csv'), sep=';')

    for m, df in avg_results_compare_string_lengths.items():
        # saves results as csv
        df.to_csv(os.path.join(process_output_target,
                  f'{m}_compare-string-lengths.csv'), sep=';')

        df_T = df.transpose()

        fig, ax = plt.subplots()
        for p in population_range:
            ax.plot(evaluation_range, df_T[p], label=str(
                p), marker='^', linestyle='dotted')

        ax.set_xlabel('# de Avaliações')
        ax.set_ylabel(m)
        ax.set_title(f'{m} - compare-string-lengths')
        ax.legend()

        # generate graphics
        ax.plot()
        plt.savefig(f'{m}_compare-string-lengths')


def verify() -> None:
    fileList = list(filter(lambda x: x.endswith(
        '.result.json'), os.listdir(hotgp_output_path)))
    failed_tests = []

    for f_name in fileList:
        _, eval_num, _, benchmark = re.search(
            file_name_regex, f_name).groups()
        if benchmark not in benchmarks:
            continue
        with open(hotgp_output_path + '/' + f_name) as file:
            best_data = json.load(file)
            if int(best_data['totalEvals']) > int(eval_num):
                failed_tests.append(f_name)

    if len(failed_tests) == 0:
        print('All ok')
    else:
        print('The following benchmarks have failed:')
        for f in failed_tests:
            print(f)
