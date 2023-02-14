from datetime import datetime
import os

class Logger:

    """ Class to manage log generation. Call as a function to initialize a new
    log. """
    def __init__(self):
        self.log_string = f"""TUFLOW Ensemble Log Generated on {datetime.now()}.
        \n===================================================================\n"""

    def log(self, msg: str):
        """ Add given msg to log """

        self.log_string += "\n" + msg + "\n"

    def print_log(self):
        """ Dump log text in current state to console. """

        print(self.log_string)

    def write_to_txt(self, output_folder):
        """ Output log as a .txt file in specified folder. """

        filename = os.path.join(output_folder, 'log.txt')

        with open(filename, 'w+') as f:
            f.write(self.log_string)
