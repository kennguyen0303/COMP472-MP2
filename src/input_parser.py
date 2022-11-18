"""
Class InputParser for parsing input file
"""


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
