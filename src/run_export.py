import app
from logger import Logger

def export(log):
    discover = app.Handler()    
    discover.export_data()

if __name__ == '__main__':
    log = Logger(name="run_export", debug=True)
    export(log)