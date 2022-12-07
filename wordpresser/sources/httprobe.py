import subprocess
import logging

class Httprobe():
    
    def __init__(self, details):
        self.wordpresser = [details["wordpresser"], "httprobe"]
          
    def httprobe(self):
        '''
        Combines wmap|cycognito|amass|terminus hosts into discovered_hosts.out
        Runs Httprobe to find live webhosts and outputs to webhosts.txt 
        '''
        logging.info("Running Httprobe...")
        try:
            subprocess.call(self.wordpresser)
            logging.info("Finished Httprobe")
        except Exception as e:
            logging.error("***Httprobe*** httprobe: [{}]".format(e))

def runHttprobe(details):
    '''
    Runs Httprobe and outputs results to webhosts.txt
    '''
    try:
        httprobe = Httprobe(details)
        httprobe.httprobe()
    except Exception as e:
        logging.error("***Httprobe*** runHttprobe: [{}]".format(e))
