from run_discovery import discovery
from run_vulnscan import vulnscan
from run_alerts import alerts
from run_export import export
from logger import Logger


if __name__ == '__main__':
    log = Logger(name="run_wordpresser", debug=True)
    discovery(log)
    vulnscan(log)
    export(log)
    alerts(log)