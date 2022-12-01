"""
Module for reporting the outputs
"""
# Excel file
# Each solution: 1 search-path, 1 solution-path
from pandas import Series, DataFrame
from input_parser import StateExtractor
from search_algos import UCS


class OutputReporter:
    """
    Class for reporting outputs
    """

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir

    def export_solution_file(self, file_name: str, search_algo: UCS, runtime: float):
        """
        Export a solution file for a search algorithm
        """
        line_separator = "--------------------------------------------------------------------------------\n"
        tmp_extractor = StateExtractor(search_algo.ori_input)
        solution_path_df = self.summarize_solution_path(search_algo)
        txt_to_print = []
        txt_to_print.append(line_separator)
        txt_to_print.append(
            "\nInitial board configuration: " + search_algo.ori_input + "\n"
        )
        txt_to_print.append("!\n\n")
        txt_to_print.append(tmp_extractor.get_curr_layout_shape())
        txt_to_print.append("\n\n")

        # fuels
        txt_to_print.append("Car fuel available: " + tmp_extractor.get_fuels() + "\n\n")
        txt_to_print.append("Runtime: " + str(runtime) + " seconds\n")
        txt_to_print.append(
            "Search path length: " + str(search_algo.state_count) + " states\n"
        )
        txt_to_print.append(
            "Solution path length: "
            + str(len(solution_path_df.count(axis=1)))
            + " moves\n\n"
        )

        txt_to_print.append("Solution path: ")
        txt_to_print.append(str(solution_path_df.details.to_list()))
        txt_to_print.append("\n\n")
        txt_to_print.append(
            solution_path_df.to_string(header=False, index=False, justify="start")
        )
        txt_to_print.append("\n")
        # for i, step in enumerate(solution_path):
        #     line = details_list[i] + "          " + step
        #     txt_to_print.append(line)
        #     txt_to_print.append("\n")

        txt_to_print.append(
            "\nFuel used: " + search_algo.final_state.get_fuels() + "\n\n"
        )

        txt_to_print.append(search_algo.final_state.get_curr_layout_shape())
        txt_to_print.append("\n\n" + line_separator)

        with open(
            self.root_dir + file_name, mode="w", encoding="utf-8"
        ) as file_handler:
            file_handler.writelines(txt_to_print)

    def summarize_solution_path(self, search_algo: UCS):
        """
        Generate the solution path
        """
        solution_path = []
        details = []
        curr_step = search_algo.final_state.get_curr_layout_str()

        while True:
            solution_path.append(curr_step)
            curr_step, message_details = search_algo.closed_list.get(
                curr_step, ("", "")
            )  # receive the parent, note: detail of the child and curr_step is now the parent
            if curr_step == "":
                solution_path.pop()
                break

            details.append(message_details)

        return DataFrame(data={"details": details[::-1], "path": solution_path[::-1]})
