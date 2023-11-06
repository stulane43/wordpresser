import app
from logger import Logger

def vulnscan(log):
    discover = app.Handler()    
    discover.wpscan_plugin_vuln_scan()
    discover.wordpress_plugin_vulns_update()
    discover.stored_procs()    

if __name__ == '__main__':
    log = Logger(name="run_vulnscan", debug=True)
    vulnscan(log)