#!/usr/bin/python3

"""
Measure the performance of a project 3 pzip binary
"""

from argparse import ArgumentParser
from resource import getrusage as resource_usage, RUSAGE_CHILDREN
from subprocess import run
from time import time as timestamp


def main():
    # Parse arguments
    parser = ArgumentParser(description="Measure the performance of a project 3 pzip binary")
    parser.add_argument("binary", type=str, help="Path of the binary to measure")
    parser.add_argument("input", type=str, help="Path of input file")
    parser.add_argument("output", type=str, help="Path to save output to")
    parser.add_argument("threads", type=int, help="Number of threads to use")

    res = parser.parse_args()

    # Get resource usage
    start_time, start_resources = timestamp(), resource_usage(RUSAGE_CHILDREN)

    # Run the binary
    run_result = run([
        res.binary,
        res.input,
        res.output,
        str(res.threads)
      ])

    if run_result.returncode != 0:
        print(f"Execution failed with error code {run_result.returncode}")
        exit(run_result.returncode)

    # Get resource usage
    end_resources, end_time = resource_usage(RUSAGE_CHILDREN), timestamp()

    real_time = end_time - start_time
    sys_time = end_resources.ru_stime - start_resources.ru_stime
    user_time = end_resources.ru_utime - start_resources.ru_utime
    pe = ((user_time + sys_time) / real_time) / res.threads

    print(f"Wall time: {real_time:.5f} seconds")
    print(f"CPU Time (System): {sys_time:.5f}  seconds")
    print(f"CPU Time (User): {user_time:.5f} seconds")
    print(f"Number of threads: {res.threads}")
    print(f"Parallel efficiency (PE): {pe:.5f}")


if __name__ == "__main__":
    main()
