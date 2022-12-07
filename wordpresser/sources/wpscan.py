import wordpresser.database.commands as db
import concurrent.futures
import subprocess
import logging
import json
import sys
import os

class Wpscan():
    
    def __init__(self, details):
        self.details = details
        self.wordpresserBasicAuth = [details["wordpresser"], "wpscan_basicauth_required"]
        self.wordpresserRedirects = [details["wordpresser"], "wpscan_redirects"]
        self.wordpresserFilter = [details["wordpresser"], "wpscan_clean"]
        self.basicAuthRequiredPath = "{}/basic_auth_required.out".format(details["outPath"])
        self.webhostsPath = "{}/webhosts.txt".format(details["outPath"])
        self.manualWebhostsPath = "{}/manual_sites.json".format(details["configPath"])
        self.discOutPath = "{}/wpscan/discovery".format(details["outPath"])
        self.vulnOutPath = "{}/wpscan/vulns".format(details["outPath"])
        self.sitesPath = "{}/wpscan.out".format(details["outPath"])
        self.redirectsPath = "{}/og_redirects.out".format(details["outPath"])
        self.apiKey = details["wpscanAPI"]
        self.discAsType = {
            'source': 'string',
            'site': 'string',
            'redirection': 'string',
            'ip': 'string',
            'wp_version': 'string',
            'plugins': 'int',
            'last_seen': 'datetime64[s]',
            'valid_site': 'bool'
        }
        self.pluginAsType = {
            'source': 'string',
            'site': 'string',
            'plugin': 'string',
            'location': 'string',
            '_version_': 'string',
            'latest_version': 'string',
            'last_updated': 'datetime64[ns]',
            'outdated': 'bool',
            'last_seen': 'datetime64[s]'
        }
        self.wpVulnAsType = {
            'site': 'string',
            'wp_version': 'string',
            'severity': 'string',
            'cve': 'string',
            'finding': 'string',
            'fixed_in': 'string',
            'reference': 'string',
            'last_seen': 'datetime64[s]'
        }
        self.wpPluginVulnAsType = {
            'site': 'string',
            'plugin': 'string',
            '_version_': 'string',
            'cve': 'string',
            'finding': 'string',
            'fixed_in': 'string',
            'reference': 'string',
            'last_seen': 'datetime64[s]'
        }
        self.redirectsAsType = {
            'site': 'string',
            'redirection': 'string'
        }
        
    def __identify(self, webhost):
        '''
        Discovers webhosts that run WordPress
        - Outputs to out/wpscan/*.discover.wp.json
        '''
        try:
            subprocess.call([self.details["wpscan"], webhost, self.discOutPath])
        except Exception as e:
            logging.error("***Wpscan*** __identify: [{}]".format(e))

    def __basicAuthIdentify(self, webhost):
        '''
        Discovers webhosts that run WordPress with basic auth creds
        - Outputs to out/wpscan/*.discover.wp.json
        '''
        try:
            subprocess.call([self.details["wpscan"], webhost, self.discOutPath, self.details["wpscanBasicAuthCreds"]])
        except Exception as e:
            logging.error("***Wpscan*** __identify: [{}]".format(e))

    def __vulns(self, site: str):
        '''
        Runs wpscan to find any plugin vulnerabilities on wordpress site
        '''
        try:
            subprocess.call([self.details["wpscanVulns"], site, self.vulnOutPath, self.apiKey])
            for file in os.listdir(self.vulnOutPath):
                _split = site.split('/')
                _site = _split[2]
                if _site in file:
                    jsonPath = os.path.join(self.vulnOutPath, file)
                    jsonFile = open(jsonPath)
                    jsonData = json.load(jsonFile)
                    vuln_api = jsonData['vuln_api']
                    if 0 < vuln_api['requests_remaining'] > 10:
                        if self.apiKey == self.details['wpscanAPI']:
                            logging.info("Switching API Keys...")
                            self.apiKey = self.details['wpscanAPI2']
                        else:
                            sys.exit("*****API Keys ran out of requests for today...*****")    
        except Exception as e:
            logging.error("***Wpscan*** __vulns: [{}]".format(e))
            
    def __threadVulns(self, sites):
        '''
        Threads __vulns function to get faster results
        '''
        logging.info("Running Wpscan Vulns...")
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                executor.map(self.__vulns, sites)
        except Exception as e:
            logging.error("***Wpscan*** __threadVulns: [{}]".format(e))
            
    def __threadIdentify(self, webhosts, basicAuth=False):
        '''
        Threads __identify function to get faster results
        
        Discovers webhosts that run WordPress
        - Outputs to out/wpscan/*.discover.wp.json
        '''
        logging.info("Running Wpscan discovery...")
        try:
            if basicAuth:
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    executor.map(self.__basicAuthIdentify, webhosts)
            else:
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    executor.map(self.__identify, webhosts)
        except Exception as e:
            logging.error("***Wpscan*** __threadIdentify: [{}]".format(e))
            
    def __findRedirects(self):
        '''
        Searches through results from __identify for redirects
        - Outputs list of redirects to redirects.txt
        '''
        logging.info("Finding redirects...")
        try:
            subprocess.call(self.wordpresserRedirects)
            redirects = db.removeDupRedirects("{}/redirects.txt".format(self.details["outPath"]))
            return redirects
        except Exception as e:
            logging.error("***Wpscan*** findRedirects: [{}]".format(e))
            
    def __filterWpSites(self):
        '''
        Removes non WordPress sites
        - outputs WordPress sites to wpscan.out
        '''
        logging.info("Removing non WordPress sites...")
        try:
            subprocess.call(self.wordpresserFilter)
        except Exception as e:
            logging.error("***Wpscan*** filterWpSites: [{}]".format(e))
            
    def __formatDiscData(self):
        '''
        Formats Wpscan identify data into tmp data table
        '''
        siteList = []
        try:
            for file in os.listdir(self.discOutPath):
                if "discover.wp.json" in file:
                    jsonPath = os.path.join(self.discOutPath, file)
                    jsonFile = open(jsonPath)
                    jsonData = json.load(jsonFile)
                    try:
                        wpVersion = jsonData["version"]["number"]
                    except:
                        wpVersion = None
                    siteData = {
                        "source": "wpscan",
                        "site": jsonData["target_url"],
                        "redirection": jsonData["effective_url"],
                        "ip": jsonData["target_ip"],
                        "wp_version": wpVersion,
                        "plugins": len(jsonData["plugins"]),
                        "last_seen": jsonData["stop_time"],
                        "valid_site": True
                    }
                    siteList.append(siteData)
            return siteList
        except Exception as e:
            logging.error("***Wpscan*** formatDiscData: [{}]".format(e))
            
    def __formatRedirects(self):
        '''
        Formats Wpscan redirects into tmap data table
        '''
        siteList = []
        try:
            with open(self.redirectsPath) as f:
                sites = f.read().splitlines()
            for site in sites:
                split_site = site.split(" - ")
                siteData = {
                    "site": split_site[0],
                    "redirection": split_site[1]
                }
                siteList.append(siteData)
            return siteList
        except Exception as e:
            logging.error("***Wpscan*** __formatRedirects: [{}]".format(e))
            
    def __formatPluginData(self):
        '''
        Formats Wpscan plugin data into tmp data table
        '''
        pluginList = []
        try:
            for file in os.listdir(self.discOutPath):
                if "discover.wp.json" in file:
                    jsonPath = os.path.join(self.discOutPath, file)
                    jsonFile = open(jsonPath)
                    jsonData = json.load(jsonFile)
                    for p in jsonData['plugins']:
                        plugin = jsonData['plugins'][p]
                        try:
                            version = plugin['version']['number']
                        except:
                            version = None
                        pluginData = {
                            'source': 'wpscan',
                            'site': jsonData['target_url'],
                            'plugin': plugin['slug'],
                            'location': plugin['location'],
                            '_version_': version,
                            'latest_version': plugin['latest_version'],
                            'last_updated': plugin['last_updated'],
                            'outdated': plugin['outdated'],
                            'last_seen': jsonData['stop_time']
                        }
                        pluginList.append(pluginData)
            return pluginList
        except Exception as e:
            logging.error("***database commands*** formatPluginData: [{}]".format(e))
            
    def __formatVulnData(self):
        '''
        Formats Wpscan Vulnerability data into tmp Data table
        '''
        vulnList = []
        pluginVulnList = []
        try:
            for file in os.listdir(self.vulnOutPath):
                if "vulns.wp.json" in file:
                    jsonPath = os.path.join(self.vulnOutPath, file)
                    jsonFile = open(jsonPath)
                    jsonData = json.load(jsonFile)
                    wpVersionData = jsonData["version"]
                    try:
                        wp_version = jsonData["version"]["number"]
                    except:
                        wp_version = None
                    for vulnerability in wpVersionData["vulnerabilities"]:
                        try:
                            cve = vulnerability["references"]["cve"][0]
                        except:
                            cve = None
                        try:
                            reference = vulnerability["references"]["url"][0]
                        except:
                            reference = None
                        siteVulnData = {
                            'site': jsonData['target_url'],
                            'wp_version': wp_version,
                            'severity': None,
                            'cve': 'cve-{}'.format(cve),
                            'finding': vulnerability['title'],
                            'fixed_in': vulnerability['fixed_in'],
                            'reference': reference,
                            'last_seen': jsonData['stop_time']       
                        }
                        vulnList.append(siteVulnData)
                    for p in jsonData['plugins']:
                        plugin = jsonData['plugins'][p]
                        try:
                            version = plugin['version']['number']
                        except:
                            version = None
                        for vuln in plugin['vulnerabilities']:
                            try:
                                pluginCve = vuln['references']['cve'][0]
                            except:
                                pluginCve = None
                            try:
                                pluginReference = vuln['references']['url'][0]
                            except:
                                pluginReference = None
                            pluginData = {
                                'site': jsonData['target_url'],
                                'plugin': plugin['slug'],
                                '_version_': version,
                                'cve': pluginCve,
                                'finding': vuln['title'],
                                'fixed_in': vuln['fixed_in'],
                                'reference': pluginReference,
                                'last_seen': jsonData['stop_time']
                            }
                            pluginVulnList.append(pluginData)
            return {'wpVulns': vulnList, 'pluginVulns': pluginVulnList}
        except Exception as e:
            logging.error("***Wpscan*** __formatVulnData: [{}]".format(e))
            
    def __findBasicAuthRequired(self):
        '''
        Finds all wpscan results that required Basic Auth Credentials and then runs wpscan again with required creds
        '''
        logging.info("Finding Basic Auth Protected Sites...")
        try:
            subprocess.call(self.wordpresserBasicAuth)
            with open(self.basicAuthRequiredPath) as f:
                basicAuthRequired = f.read().splitlines()
            return basicAuthRequired
        except Exception as e:
            logging.error("***Wpscan*** findBasicAuthRequired: [{}]".format(e))
    
    def wpscanDiscovery(self, dbInsert: bool, manualScan: bool):
        '''
        Runs Wpscan to find WordPress sites and associated plugins
        '''
        logging.info("Running Wpscan...")
        try:
            if manualScan:
                with open(self.manualWebhostsPath) as f:
                    hosts = json.load(f)
                    webhosts = hosts['manual_sites']
            else:
                with open(self.webhostsPath) as f:
                    webhosts = f.read().splitlines()
            self.__threadIdentify(webhosts)
            basicAuthRequired = self.__findBasicAuthRequired()
            if basicAuthRequired != []:
                self.__threadIdentify(basicAuthRequired, True)
            redirects = self.__findRedirects()
            self.__threadIdentify(redirects)
            redirectsData = self.__formatRedirects()
            db.insertData(redirectsData, "tmp_redirects", "site", self.redirectsAsType, dupRemove=False)
            self.__filterWpSites()
            db.cleanWpscanData(self.discOutPath, "{}/wpscan.out".format(self.details["outPath"]))
            siteList = self.__formatDiscData()
            pluginList = self.__formatPluginData()
            if dbInsert:
                db.insertData(siteList, "tmp_wpscan_sites", "site", self.discAsType)
                logging.info("Inserted Wpscan discovery data")
                db.insertData(pluginList, "tmp_wpscan_plugins", "site", self.pluginAsType, dupRemove=False)
                logging.info("Inserted Wpscan plugin data")
            else:
                logging.info("Skipped Wpscan insert")
        except Exception as e:
            logging.error("***Wpscan*** wpscanDiscovery: [{}]".format(e))
            
    def wpscanVulnerability(self, dbInsert: bool):
        '''
        Runs Wpscan to find WordPress vulnerabilities on discovered sites
        '''
        logging.info("Running Wpscan...")
        try:
            with open(self.sitesPath) as s:
                sites = s.read().splitlines()
            self.__threadVulns(sites)
            vulns = self.__formatVulnData()
            if dbInsert:
                db.insertData(vulns['wpVulns'], "tmp_wpscan_vulns", "site", self.wpVulnAsType, dupRemove=False)
                logging.info("Inserted Wpscan vuln data")
                db.insertData(vulns['pluginVulns'], "tmp_wpscan_plugin_vulns", "site", self.wpPluginVulnAsType, dupRemove=False)
                logging.info("Inserted Wpscan plugin vuln data")
            else:
                logging.info("Skipped Wpscan vuln insert")
        except Exception as e:
            logging.error("***Wpscan*** wpscanVulnerability: [{}]".format(e))
            
def runWpscan(details, dbInsert=False, discScan=False, vulnScan=False, manualScan=False):
    '''
    Runs Wpscan and outputs results to out/wpscan/*.discover.wp.json
    - dbInsert: Insert data to database (Default: False)
    '''
    try:
        wpscan = Wpscan(details)
        if discScan:
            wpscan.wpscanDiscovery(dbInsert, manualScan)
        if vulnScan:
            wpscan.wpscanVulnerability(dbInsert)
    except Exception as e:
        logging.error("***Wpscan*** runWpscan: [{}]".format(e))