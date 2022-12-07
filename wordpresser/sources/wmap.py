import wordpresser.database.commands as db
import logging

class Wmap():
    
    def __init__(self, details):
        self.details = details
        self.outPath = "{}/wmap.out".format(details["outPath"])
        self.tmpTable = "tmp_wmap_sites"
        
    def wmap(self, dbInsert: bool):
        '''
        Gets Unique wordpress assets from Wmap
        '''
        logging.info("Running Wmap...")
        try:
            assets = db.readWmap(self.details["wmapQuery"])
            assetsDict = assets.to_dict('records')
            db.outFile(assetsDict, self.outPath, "wp_site")
            if dbInsert:
                db.insertData(assetsDict, self.tmpTable, "wp_site")
                logging.info("Inserted Wmap data")
            else:
                logging.info("Skipped Wmap insert")
        except Exception as e:
            logging.error("***Wmap*** __wmap: [{}]".format(e))
        
def runWmap(details, dbInsert=False):
    '''
    Runs Wmap and outputs results to wmap.out
    - dbInsert: Insert data to database (Default: False)
    '''
    try:
        wmap = Wmap(details)
        wmap.wmap(dbInsert)
    except Exception as e:
        logging.error("***Wmap*** runWmap: [{}]".format(e))