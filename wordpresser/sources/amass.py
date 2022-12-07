import wordpresser.database.commands as db
import subprocess
import logging

class Amass():
    
    def __init__(self, details):
        self.wordpresser = [details["wordpresser"], "amass"]
        self.outPath = "{}/amass.txt".format(details["outPath"])
        self.tmpTable = "tmp_amass_sites"
        self.dfAstype = {'site': 'string'}
            
    def amass(self, dbInsert: bool):
        '''
        Runs Amass intel and inserts data into tmp db table
        '''
        logging.info("Running Amass...")
        try:
            subprocess.call(self.wordpresser)
            if dbInsert:
                db.insertFileData(self.tmpTable, self.dfAstype, path=self.outPath)
                logging.info("Inserted Amass data")
            else:
                logging.info("Skipped Amass insert")
        except Exception as e:
            logging.error("***Amass*** __amass: [{}]".format(e))
        
def runAmass(details, dbInsert=False):
    '''
    Runs Amass and outputs results to amass.out
    - dbInsert: Insert data to database (Default: False)
    '''
    try:
        amass = Amass(details)
        amass.amass(dbInsert)
    except Exception as e:
        logging.error("***Amass*** runAmass: [{}]".format(e))