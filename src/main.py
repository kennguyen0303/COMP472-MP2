"""
Something
"""
from datetime import datetime
from input_parser import InputParser
from search_algos import UCS
from reporter import OutputReporter

if __name__ == "__main__":
    FILE_PATH = (
        "/home/n_thekie/Desktop/school/comp 472/COMP472-MP2/Sample/sample-input.txt"
    )
    INPUTS = InputParser.parse(FILE_PATH)
    reporter = OutputReporter(
        root_dir="/home/n_thekie/Desktop/school/comp 472/COMP472-MP2/outputs/"
    )
    sol_count = 0
    for idx, input_str in enumerate(INPUTS):
        if idx == 2:
            break
        print("\n-------- NEW INPUT--------\n")
        curr_time = datetime.now()
        usc = UCS()
        usc.search_ucs(input_str)
        run_time = (datetime.now() - curr_time).total_seconds()
        sol_count += 1
        print(usc.is_final_state_reached)
        print(usc.state_count)
        print("Take: ", run_time)
        filename = "ucs-sol-" + str(sol_count) + ".txt"
        reporter.export_solution_file(filename, usc, run_time)
