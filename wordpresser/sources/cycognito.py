import wordpresser.database.commands as db
import urllib3
import requests
import logging
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PAGES = 1
PAGINATION = 1000

class Cycognito():
    
    def __init__(self, details):
        self.details = details
        self.outPath = "{}/cycognito.out".format(details["outPath"])
        self.offset = 0
        self.tmpTable = "tmp_cycognito_sites"
        self.headers = {
            "Content-Type": "application/frdy+json", 
            "Accept": "application/frdy+json"
        }
        self.dfAstype = {
            'site': 'string',
            'ip': 'string',
            'hosting_provider': 'string',
            'first_seen': 'datetime64[ns]',
            'last_seen': 'datetime64[ns]'
        }
        
    def __request(self, method: str, endpoint: str, params=None, data=None):
        '''
        Handles any api action, post, put, and get.
        Returns: response
        '''
        try:
            res = requests.request(method, endpoint, headers=self.headers, params=params, data=data, verify=self.details['certVerify'])
            return res
        except Exception as e:
            logging.error("***Cycognito*** request: [{}]".format(e))
            
    def __queryAssets(self):
        '''
        Calls Cycgonito API to query wordpress assets from Bertelsmann realm
        '''
        try:
            while self.offset < PAGES:
                params = {
                    "key": self.details["cycognitoAPI"],
                    "count": PAGINATION,
                    "offset": self.offset
                }
                data = '[{"op":"in","field":"platform-names","values":["WordPress"]}]'
                res = self.__request("post", self.details["cycognitoEndpoint"], params, data)
                res.raise_for_status()
                res = res.json()
                if not res:
                    break
                yield from res
                self.offset = self.offset + 1
        except Exception as e:
            logging.error("***Cycognito*** __queryAssets: [{}]".format(e))
            
    def cycognito(self, dbInsert: bool):
        '''
        Gets unique wordpress assets from Cycognito
        '''
        logging.info("Running Cycognito")
        assetList = []
        try:
            assets = list(self.__queryAssets())
            for asset in assets:
                for domain in asset['domain-names']:
                    if '.com' in domain:
                        re.sub('^(http|https)://|/', '', domain)
                        assetList.append({
                            'site': domain,
                            'ip': asset['ip'],
                            'hosting_provider': asset['owned-by'],
                            'first_seen': asset['first-seen'],
                            'last_seen': asset['last-seen']
                            })
            db.outFile(assetList, self.outPath, "site")
            uAssetList = db.removeDups(assetList, True, "site")
            if dbInsert:
                db.insertFileData(self.tmpTable, self.dfAstype, _list=uAssetList)
                logging.info("Inserted Cycognito data")
            else:
                logging.info("Skipped Cycognito insert")
        except Exception as e:
            logging.error("***Cycognito*** __getAssets: [{}]".format(e))

def runCycognito(details, dbInsert=False):
    '''
    Runs Cycognito and outputs results to cycognito.out
    - dbInsert: Insert data to database (Default: False)
    '''
    try:
        cycognito = Cycognito(details)
        cycognito.cycognito(dbInsert)
    except Exception as e:
        logging.error("***Cycognito*** runCycognito: [{}]".format(e))