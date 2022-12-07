import logging
import wordpresser.database.commands as db

class WordPress():
    
    def __init__(self, details):
        self.query = details["allSitesQuery"]
        self.outPath = "{}/wordpresser.out".format(details["outPath"])
        
    def getSitesSeen(self):
        '''
        looks in wp database and returns all sites into dataframe
        '''
        logging.info("Running allSites search...")
        try:
            sitesSeen = db.readWordPressSites(query=self.query)
            sitesSeenDict = sitesSeen.to_dict('records')
            db.outFile(sitesSeenDict, self.outPath, "site")
            return sitesSeenDict
        except Exception as e:
            logging.error("***WordPress*** allSites: [{}]".format(e))
            
    def getTableData(self, table):
        '''
        Looks up wp data and returns into dataframe
        '''
        logging.info("Running database search...")
        try:
            query = "SELECT * FROM {}".format(table)
            tableData = db.readWordPressSites(query)
            return tableData
        except Exception as e:
            logging.error("***WordPress*** getTableData: [{}]".format(e))
            
def runWordPress(details):
    '''
    Pulls latest wordpress_sites data into dataframe
    - If a site has been seen in the last 7 days, add it to a 'DO NOT RUN' list
    - any site in that list will not be scanned further to save time
    '''
    try:
        wp = WordPress(details)
        sitesSeen = wp.getSitesSeen()
        return sitesSeen
    except Exception as e:
        logging.error("***WordPress*** runWordPress: [{}]".format(e))
        
def getWordPress_database(details, table):
    '''
    returns any table from wordpresser database in dataframe
    - Provide database table name {table}
    '''
    try:
        wp = WordPress(details)
        tableData = wp.getTableData(table)
        return tableData
    except Exception as e:
        logging.error("***WordPress*** getWordPress_database: [{}]".format(e))