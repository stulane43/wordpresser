import json
from .logger import Logger
from pathlib import Path

class Connector(Logger):

    def __init__(self, name, _log=True):
        super().__init__(name, _log)
        current_path = Path().absolute()
        config = Path(f"{str(current_path)}/wordpresser/configuration/config.json")
        self.details = json.load(open(config))