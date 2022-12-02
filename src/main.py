"""
Something
"""
from datetime import datetime
from input_parser import InputParser
from search_algos import GBFS, AlgoA, UCS, calculate_heuristic_1
from reporter import OutputReporter


def run_ucs(inputs: list, reporter: OutputReporter):
    """
    Function for running UCS in main with some format
    """
    for idx, input_str in enumerate(inputs):
        print("\n-------- NEW INPUT--------\n")
        curr_time = datetime.now()
        ucs = UCS()
        ucs.search(input_str)
        run_time = (datetime.now() - curr_time).total_seconds()
        print(ucs.is_final_state_reached)
        print(len(ucs.closed_list))
        print("Take: ", run_time)
        sol_count = idx + 1
        file_solution_name = "ucs-sol-" + str(sol_count) + ".txt"
        file_search_name = "ucs-search-" + str(sol_count) + ".txt"
        reporter.export_solution_file(file_solution_name, ucs, run_time)
        reporter.export_search_path_file(file_search_name, ucs)


def run_algorithm_a(inputs: list, reporter: OutputReporter):
    """
    Function for Algorithm A in main with some format
    """
    for idx, input_str in enumerate(inputs):
        print("\n-------- NEW INPUT--------\n")
        curr_time = datetime.now()
        a = AlgoA(heuristic_function=calculate_heuristic_1)
        a.search(input_str)
        run_time = (datetime.now() - curr_time).total_seconds()
        print(a.is_final_state_reached)
        print(len(a.closed_list))
        print("Take: ", run_time)
        sol_count = idx + 1
        file_solution_name = "a-h1-sol-" + str(sol_count) + ".txt"
        file_search_name = "a-h1-search-" + str(sol_count) + ".txt"
        reporter.export_solution_file(file_solution_name, a, run_time)
        reporter.export_search_path_file(file_search_name, a)


def run_greedy_bfs(inputs: list, reporter: OutputReporter):
    """
    Function for Algorithm Greedy BFS in main with some format
    """
    for idx, input_str in enumerate(inputs):
        print("\n-------- NEW INPUT--------\n")
        curr_time = datetime.now()
        gbfs = GBFS(heuristic_function=calculate_heuristic_1)
        gbfs.search(input_str)
        run_time = (datetime.now() - curr_time).total_seconds()
        print(gbfs.is_final_state_reached)
        print(len(gbfs.closed_list))
        print("Take: ", run_time)
        sol_count = idx + 1
        file_solution_name = "gbfs-h1-sol-" + str(sol_count) + ".txt"
        file_search_name = "gbfs-h1-search-" + str(sol_count) + ".txt"
        reporter.export_solution_file(file_solution_name, gbfs, run_time)
        reporter.export_search_path_file(file_search_name, gbfs)


if __name__ == "__main__":
    FILE_PATH = (
        "/home/n_thekie/Desktop/school/comp 472/COMP472-MP2/Sample/sample-input.txt"
    )
    INPUTS = InputParser.parse(FILE_PATH)
    reporter = OutputReporter(
        root_dir="/home/n_thekie/Desktop/school/comp 472/COMP472-MP2/outputs/"
    )
    run_greedy_bfs(INPUTS, reporter)
