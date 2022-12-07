import wordpresser.database.commands as db
import concurrent.futures
import subprocess
import logging

class Terminus():
    
    def __init__(self, details, doNotScanList):
        self.details = details
        self.doNotScanList = doNotScanList
        self.outPath = "{}/terminus.out".format(details["outPath"])
        self.pluginOutPath = "{}/plugins.csv".format(details["outPath"])
        self.sitesTmpTable = "tmp_terminus_sites"
        self.pluginsTmpTable = "tmp_terminus_plugins"
        self.sitesDfAstype = {'site': 'string'}
        self.envs = ["live", "test", "dev"]
        self.csvHeaders = ['site', 'plugin', 'status', '_update_', '_version_']
        self.pluginsDfAstype = {
            'site': 'string',
            'plugin': 'string',
            'status': 'string',
            '_update_': 'string',
            '_version_': 'string'
        }
        
    def __terminus(self, env: str):
        '''
        Gets dev/test/live Pantheon webhosts and all plugins
        - Outputs webhosts to terminus.out 
        - Outputs plugins to plugins.csv
        '''
        try:
            subprocess.call([self.details["terminus"], env])
        except Exception as e:
            logging.error("***Terminus*** __terminus: [{}]".format(e))

    def threadTerminus(self, dbInsert: bool):
        '''
        Threads __terminus function to get faster results
        
        Gets dev/test/live Pantheon webhosts and all plugins
        - Outputs webhosts to terminus.out
        - Outputs plugins to plugins.csv
        '''
        logging.info("Running Terminus...")
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(self.__terminus, self.envs)
            db.removeDupHeaders(self.pluginOutPath)
            if dbInsert:
                db.insertFileData(self.sitesTmpTable, self.sitesDfAstype, path=self.outPath)
                db.insertCsvData(self.pluginOutPath, self.pluginsTmpTable, self.csvHeaders, self.pluginsDfAstype)
                logging.info("Inserted Termninus data")
            else:
                logging.info("Skipped Terminus insert")
        except Exception as e:
            logging.error("***Terminus*** __threadTerminus: [{}]".format(e))
            
def runTerminus(details, doNotScanList, dbInsert=False):
    '''
    Runs Terminus and outputs results to terminus.out and plugins.csv
    - dbInsert: Insert data to database (Default: False)
    '''
    try:
        terminus = Terminus(details, doNotScanList)
        terminus.threadTerminus(dbInsert)
    except Exception as e:
        logging.error("***Terminus*** runTerminus: [{}]".format(e))