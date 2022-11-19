"""
Class InputParser for parsing input file
"""
from enum import Enum


class InputParser:
    """
    Class InputParser for parsing input file
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def parse(filepath: str):
        """
        parse the input txt, return the list of input configurations
        """
        outputs = []
        with open(filepath, mode="r", encoding="utf-8") as file:
            while True:
                line = file.readline()
                if line == "":
                    break  # reach EoF

                if line == "\n" or "#" == line[0]:
                    continue  # skip comments

                # if here, it's the input
                outputs.append(line.strip())

        return outputs


class MovingDirection(Enum):
    """
    Enum class for the direction
    """

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class Vehicle:
    """
    A vehicle
    """

    def __init__(
        self,
        name: str,
        last_point_loc: tuple,
        size=1,
        mov_dir=MovingDirection.HORIZONTAL,
        fuel=100,
    ) -> None:
        self.name = name
        self.size = size
        self.last_point_loc = last_point_loc
        self.mov_dir = mov_dir
        self.fuel = fuel

    def add_new_part(self, new_part_loc: tuple):
        """
        Add a new part of the vehicle
        """
        if (
            new_part_loc[0] != self.last_point_loc[0]
            and self.mov_dir != MovingDirection.VERTICAL
        ):  # same row
            self.mov_dir = MovingDirection.VERTICAL

        self.size += 1
        self.last_point_loc = new_part_loc

    def __str__(self):
        return (
            "vehicle name: "
            + self.name
            + " , size ="
            + str(self.size)
            + ", direction: "
            + str(self.mov_dir.value)
            + ", curr_fuel_level: "
            + str(self.fuel)
            + ", last_position: "
            + str(self.last_point_loc)
        )


class StateExtractor:
    """
    Class for extracting the information from a string
    """

    def __init__(self, str_input: str, size=6) -> None:
        self.input = str_input
        self.vehicles = {}
        self.size = size
        self.has_custom_fuel = False

    def convert_to_array(self):
        """
        Convert the str input into a 2-d array
        """
        curr_board = [0]*self.size  # initiate the 2-d array
        curr = 0
        for i in range(self.size):
            row = [0]*self.size
            for j in range(self.size):
                row[j] = self.input[curr]
                curr += 1
            curr_board[i] = row

        return curr_board

    def collect_vehicles(self):
        """
        Collect the vehicles info
        """
        vehicles = {}
        fuel_idx = float("inf")
        for idx, char in enumerate(self.input):
            if char == " ":
                fuel_idx = idx + 1
                break

            if char == ".":
                continue  # no need

            # define curr location
            row_pos = idx // self.size
            col_pos = idx - row_pos * self.size
            curr_loc = (row_pos, col_pos)

            if vehicles.get(char) is None:
                # initiate the new vehicle
                vehicles[char] = Vehicle(char, curr_loc)
            else:
                # if the vehicle is defined, update its part
                vehicle: Vehicle = vehicles[char]
                vehicle.add_new_part(curr_loc)

        # if has custom fuel
        while fuel_idx < len(self.input):
            veh_name = self.input[fuel_idx]
            vehicle: Vehicle = vehicles[veh_name]
            vehicle.fuel = self.input[fuel_idx + 1]
            fuel_idx += 3

        self.vehicles = vehicles
