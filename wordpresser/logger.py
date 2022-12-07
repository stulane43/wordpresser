import logging
import datetime
from pathlib import Path

class Logger:

    def __init__(self, name, _log):
        if _log:
            todaysDate = datetime.date.today().strftime("%Y-%m-%d")
            current_path = Path().absolute()
            logFile = Path(f"{str(current_path)}/wordpresser/configuration/logs/{name}_{todaysDate}.log")
            if logFile.is_file():
                logging.basicConfig(level=logging.INFO,
                                    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                                    datefmt="%m-%d %H:%M",
                                    filename=logFile)
            else:
                logging.basicConfig(level=logging.INFO,
                                    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                                    datefmt="%m-%d %H:%M",
                                    filename=logFile,
                                    filemode="w")
            # define a Handler which writes INFO messages or higher to the sys.stderr
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            # set a format which is simpler for console use
            formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
            # tell the handler to use this format
            console.setFormatter(formatter)
            # add the handler to the root logger
            logging.getLogger('').addHandler(console)
            self.log = logging.getLogger(name)
        else:
            print("Logging turned off for {}".format(name))
