from sys import argv

from process import *
from run import benchmarks


def main():
    if len(argv) < 2:
        print('Missing arguments')
        return

    mode = argv[1]
    match mode:
        case 'teste':
            print('teste')
        case 'verify':
            verify()
        case 'run-all':
            runAllBenchmarks()
        case 'run':
            if len(argv) < 3:
                print('Missing benchmark name')
            elif argv[2] not in benchmarks:
                print('Invalid benchmark')
            else:
                runBenchmark(argv[2])
        case 'process':
            process()
        case 'plot':
            print('not yet implemented')
        case _:
            print('invalid arg')


if __name__ == '__main__':
    main()
