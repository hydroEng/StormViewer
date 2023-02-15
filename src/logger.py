from datetime import datetime
import os
import pandas


class Logger:
    """ Class to manage log generation. Call as a function to initialize a new
    log. """

    def __init__(self):
        self.log_string = f"""TUFLOW Ensemble Log Generated on {datetime.now()}.
        \n===================================================================\n"""

    def log(self, msg):
        """ Add given message to log. Can handle pandas series/dataframes, strings, and lists of all the above. """

        def _write_any(msg):
            self.log_string += "\n" + msg

        def _write_sr(msg: pandas.Series):
            self.log_string += '\n' + msg.to_string() + '\n'

        def _write_df(msg: pandas.DataFrame):
            self.log_string += '\n' + msg.to_string() + '\n'

        def _write_none():
            self.log_string += '\n' + "None" + '\n'

        def _write_list(msg: list):

            if not msg:
                _write_none()

            for i in msg:

                if isinstance(i, pandas.Series):
                    _write_sr(i)
                elif isinstance(i, pandas.DataFrame):
                    _write_df(i)
                else:
                    _write_any(i)

        if isinstance(msg, pandas.Series):
            _write_sr(msg)
        elif isinstance(msg, pandas.DataFrame):
            _write_df(msg)
        elif isinstance(msg, list):
            _write_list(msg)
        else:
            _write_any(msg)

    def print_log(self):
        """ Dump log text in current state to console. """

        print(self.log_string)

    def write_to_txt(self, output_folder):
        """ Output log as a .txt file in specified folder. """

        filename = os.path.join(output_folder, 'log.txt')

        with open(filename, 'w+') as f:
            f.write(self.log_string)
