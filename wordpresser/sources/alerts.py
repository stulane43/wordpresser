import pymsteams
import wordpresser.database.commands as db
import logging

class Alerts():
    
    def __init__(self, details):
        self.query = details["newSitesQuery"]
        
    def newSites(self):
        '''
        looks in wp database and sees if there are any new sites
        '''
        logging.info("Running newSites search...")
        try:
            newSites = db.readWordPressSites(query=self.query)
            sitesDict = newSites.to_dict('records')
            return sitesDict
        except Exception as e:
            logging.error("***Alerts*** newSites: [{}]".format(e))
            
def runAlerts(details):
    '''
    Runs Amass and outputs results to amass.out
    - dbInsert: Insert data to database (Default: False)
    '''
    try:
        alerts = Alerts(details)
        newSites = alerts.newSites()
        if newSites != []:
            teamsMessage = pymsteams.connectorcard(details['alertsWebhook'])
            messageSection = pymsteams.cardsection()
            messageSection.activityTitle("New WordPress Site(s) Seen:")
            for site in newSites:
                messageSection.addFact(" ", site['site'])
            teamsMessage.addSection(messageSection)
            teamsMessage.text("WordPresser Alert!")
            teamsMessage.send()
    except Exception as e:
        logging.error("***Alerts*** runAlerts: [{}]".format(e))