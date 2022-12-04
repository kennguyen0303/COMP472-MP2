"""
Module for running puzzles and export to csv spreadsheet
"""
from datetime import datetime

from pandas import DataFrame
from input_parser import InputParser
from search_algos import (
    GBFS,
    AlgoA,
    UCS,
    GenericSearch,
    calculate_heuristic_1,
    calculate_heuristic_2,
    calculate_heuristic_3,
    calculate_heuristic_4,
)
from reporter import OutputReporter

# GLOBAL
heuristics = [
    calculate_heuristic_1,
    calculate_heuristic_2,
    calculate_heuristic_3,
    calculate_heuristic_4,
]
reporter = OutputReporter(
    root_dir="/home/n_thekie/Desktop/school/comp 472/COMP472-MP2/outputs/"
)
# list for storing columns
puzzle_col = []
algorithm_col = []
heuristic_col = []
solution_length_col = []
search_path_length_col = []
execution_time_col = []


def record_data(
    search_algo: GenericSearch,
    puzzle_number: str,
    runtime: str,
):
    """
    Record the data for a row for a run
    """
    solution_path_df = reporter.summarize_solution_path(search_algo)
    puzzle_col.append(puzzle_number)
    algorithm_col.append(search_algo.name)
    heuristic_col.append(search_algo.heuristic_name)
    solution_length_col.append(str(len(solution_path_df.count(axis=1))))
    search_path_length_col.append(str(len(search_algo.closed_list)))
    execution_time_col.append(runtime)


def run_ucs(input_str: str, puzzle_number: str):
    """
    Function for running UCS in main with some format
    """
    ucs = UCS()
    curr_time = datetime.now()
    ucs.search(input_str)
    run_time = (datetime.now() - curr_time).total_seconds()
    record_data(ucs, puzzle_number, run_time)


def run_algorithm_a(
    input_str: str,
    puzzle_number: str,
    heuristic_function,
    heuristic_number,
):
    """
    Function for Algorithm A in main with some format
    """
    algo_A = AlgoA(heuristic_function, heuristic_number)
    curr_time = datetime.now()
    algo_A.search(input_str)
    run_time = (datetime.now() - curr_time).total_seconds()
    record_data(algo_A, puzzle_number, run_time)


def run_greedy_bfs(
    input_str: str,
    puzzle_number: str,
    heuristic_function,
    heuristic_number,
):
    """
    Function for Algorithm Greedy BFS in main with some format
    """
    gbfs = GBFS(heuristic_function, heuristic_number)
    curr_time = datetime.now()
    gbfs.search(input_str)
    run_time = (datetime.now() - curr_time).total_seconds()
    record_data(gbfs, puzzle_number, run_time)


if __name__ == "__main__":
    FILE_PATH = "/home/n_thekie/Desktop/school/comp 472/COMP472-MP2/src/50-puzzles.txt"
    INPUTS = InputParser.parse(FILE_PATH)

    # running algos
    for puzzle_idx, puzzle in enumerate(INPUTS):
        run_ucs(puzzle, (puzzle_idx + 1))
        for h_idx, heuristic in enumerate(heuristics):
            run_greedy_bfs(puzzle, puzzle_idx + 1, heuristic, str(h_idx + 1))

        for h_idx, heuristic in enumerate(heuristics):
            run_algorithm_a(puzzle, puzzle_idx + 1, heuristic, str(h_idx + 1))

    # generate df
    result_df = DataFrame(
        data={
            "Puzzle Number": puzzle_col,
            "Algorithm": algorithm_col,
            "Heuristic": heuristic_col,
            "Length of the Solution": solution_length_col,
            "Length of the Search Path": search_path_length_col,
            "Execution Time (in seconds)": execution_time_col,
        }
    )

    # print(result_df.to_string(index=False))

    # csv
    result_df.to_csv("test.csv", index=False)
