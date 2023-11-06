import app
from logger import Logger

def discovery(log):
    discover = app.Handler()    
    discover.pantheon()
    discover.wordpress_sites_update()
    discover.wordpress_plugins_update()
    
if __name__ == '__main__':
    log = Logger(name="run_discovery", debug=True)
    discovery(log)