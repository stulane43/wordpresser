import app
from logger import Logger

def alerts(log):
    discover = app.Handler()    
    discover.wordpresser_alerts()

if __name__ == '__main__':
    log = Logger(name="run_alerts", debug=True)
    alerts(log)