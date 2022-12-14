"""
Module for reporting the outputs
"""
# Excel file
# Each solution: 1 search-path, 1 solution-path
from pandas import DataFrame
from input_parser import StateExtractor
from search_algos import UCS


class OutputReporter:
    """
    Class for reporting outputs
    """

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
        self.spead_sheet_df = DataFrame()

    def export_solution_file(self, file_name: str, search_algo: UCS, runtime: float):
        """
        Export a solution file for a search algorithm
        """
        line_separator = "--------------------------------------------------------------------------------\n"
        tmp_extractor = StateExtractor(search_algo.ori_input)
        solution_path_df = self.summarize_solution_path(search_algo)
        is_solvable = len(solution_path_df.count(axis=1)) > 0
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
        if not is_solvable:
            txt_to_print.append(
                "Sorry, could not solve the puzzle as specified.\nError: no solution found.\n"
            )
        txt_to_print.append("Runtime: " + str(runtime) + " seconds\n")

        if is_solvable:
            txt_to_print.append(
                "Search path length: " + str(len(search_algo.closed_list)) + " states\n"
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
            txt_to_print.append(
                "\nFuel used: "
                + search_algo.final_state.get_fuels(only_consumed=True)
                + "\n\n"
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
        fuels = []
        curr_step = search_algo.final_state.get_curr_layout_str()

        while curr_step != "":
            solution_path.append(curr_step)
            curr_state = search_algo.closed_list.get(
                curr_step, ("", "", "")
            )  # receive the parent, note: detail of the child and curr_step is now the parent
            curr_step, message_details, fuel = (
                curr_state[0],
                curr_state[1],
                curr_state[2],
            )

            if curr_step == "":
                solution_path.pop()
                break

            details.append(message_details)
            fuels.append(fuel)

        return DataFrame(
            data={
                "details": details[::-1],
                "fuels": fuels[::-1],
                "path": solution_path[::-1],
            }
        )

    def export_search_path_file(self, file_name: str, search_algo: UCS):
        """
        Export search path
        """
        search_path_df = self.get_search_path(search_algo)
        txt_to_print = []
        txt_to_print.append(
            search_path_df.to_string(header=False, index=False, justify="start")
        )
        with open(
            self.root_dir + file_name, mode="w", encoding="utf-8"
        ) as file_handler:
            file_handler.writelines(txt_to_print)

    def get_search_path(self, search_algo: UCS):
        """
        export the search path
        """
        search_strs = []
        h_vals = []
        g_vals = []
        f_vals = []
        fuel_states = []
        for state in search_algo.search_path:
            h_vals.append(state[5][1])
            g_vals.append(state[5][0])
            f_vals.append(state[0])
            search_strs.append(state[1])
            fuel_states.append(state[2])

        return DataFrame(
            data={
                "f_val": f_vals,
                "g_val": g_vals,
                "h_val": h_vals,
                "state": search_strs,
                "fuels": fuel_states,
            }
        )
