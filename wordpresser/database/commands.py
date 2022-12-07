from sqlalchemy.orm import sessionmaker
import pandas as pd
import logging
import re
import os
from .wmapdb import wmapEngine
from .wpdb import wpEngine
from . import models 

def createTables(create: bool):
    '''
    Creates app_discovery tables
    '''
    try:
        if create:
            models.Base.metadata.create_all(bind=wpEngine)
    except Exception as e:
        print(f"Error: {e}")

def callStoredProcs():
    '''
    Calls Stored Procedures in app discovery
    '''
    try:
        Session = sessionmaker(bind=wpEngine)
        session = Session()
        print("Updating Amass Table...")
        session.execute("Call UpdateAmass;")
        print("Updating Cycogito Table...")
        session.execute("Call UpdateCycognito;")
        print("Updating Wmap Table...")
        session.execute("Call UpdateWmap;")
        print("Updating Terminus Table...")
        session.execute("Call UpdateTerminus;")
        print("Updating TerminusPlugins Table...")
        session.execute("Call UpdateTerminusPlugins;")
        print("Updating Wpscan Table...")
        session.execute("Call UpdateWpscan;")
        print("Updating WpscanPlugins Table...")
        session.execute("Call UpdateWpscanPlugins;")
        print("Updating Wordpress Table...")
        session.execute("Call UpdateWordpress;")
        print("Dropping Temp Tables...")
        session.execute("Call DropTmpTables;")
        session.commit()
    except Exception as e:
        logging.error("***database commands*** callStoredProcs: [{}]".format(e))
    finally:
        session.close()

def readWmap(query: str):
    '''
    reads wordpress data from Wmap and returns dataframe
    '''
    try:
        data = pd.read_sql(query, wmapEngine)
        logging.debug("Read Wmap Data - query: {}".format(query))
        return data
    except Exception as e:
        logging.error("***database commands*** readWmap: [{}]".format(e))
        
def readWordPressSites(query: str):
    '''
    reads wordpress sites and returns any sites discovered today
    '''
    try:
        data = pd.read_sql(query, wpEngine)
        logging.debug("Read wpEngine data - query: {}".format(query))
        return data
    except Exception as e:
        logging.error("***database commands*** get_newSites: [{}]".format(e))

def insertData(_list: list, table: str, itemValue: str, asType=None, dupRemove=True):
    '''
    inserts data from list of dicts into tmp db table 
    '''
    try:
        if dupRemove:
            _list = removeDups(_list, True, itemValue)
        df = pd.DataFrame(_list)
        if asType:
            df = df.astype(asType)
        df.to_sql(table, wpEngine, if_exists="replace", index=False)
    except Exception as e:
        logging.error("***database commands*** insertData: [{}]".format(e))

def insertFileData(table: str, dfAstype: dict, _list=None, path=None):
    '''
    Inserts file data into tmp db table 
    '''
    try:
        if _list == None:
            file = open(path, "r")
            sites = file.read().splitlines()
            _list = {'site': sites}
        df = pd.DataFrame(_list)
        dfType = df.astype(dfAstype)
        dfType.to_sql(table, wpEngine, if_exists="replace", index=False)
        logging.debug("Inserted data to {}".format(table))
    except Exception as e:
        logging.error("***database commands*** insertFileData: [{}]".format(e))
        
def insertCsvData(path: str, table: str, csvHeaders: list, dfAstype: dict):
    '''
    Inserts CSV data into tmp db table
    '''
    try:
        df = pd.read_csv(path, names=csvHeaders)
        dfType = df.astype(dfAstype)
        dfType.to_sql(table, wpEngine, if_exists="replace", index=False)
        logging.debug("Inserted data to {}".format(table))
    except Exception as e:
        logging.error("***database commands*** insertCsvData: [{}]".format(e))

def outFile(_list: list, outPath: str, itemValue: str):
    '''
    Cleans assets data and outputs to file (_file)
    '''
    assetList = []
    try:
        for item in _list:
            item[itemValue] = re.sub('^(http|https)://|/', '', item[itemValue])
            item[itemValue] = re.sub('^(www\.)', '', item[itemValue])
            assetList.append(item[itemValue])
        uAssetList = removeDups(assetList, False)
        with open(outPath, "w") as file:
            file.writelines("%s\n" % i for i in uAssetList)
        return
    except Exception as e:
        logging.error("***database commands*** outFile: [{}]".format(e))
        
def removeDups(_list: list, _dict: bool, itemValue=None):
    '''
    Removes duplicates in a list
    '''
    try:
        done = set()
        uniqueList = []
        if _dict:
            for item in _list:
                if item[itemValue] not in done:
                    done.add(item[itemValue])
                    uniqueList.append(item)
        else:
            for item in _list:            
                if item not in done:
                    done.add(item)
                    uniqueList.append(item)
        logging.debug("Removed duplicates")
        return uniqueList
    except Exception as e:
        logging.error("***database commands*** removeDups: [{}]".format(e))
        
def removeDupHeaders(path: str):
    '''
    Removes duplicate headers in csv file
    '''
    try:
        with open(path, "r") as inp:
            lines = inp.readlines()
        with open(path, "w") as out:
            for line in lines:
                if not 'name' in line and not 'version' in line:
                    out.write(line)
    except Exception as e:
        logging.error("***database commands*** removeDupHeaders: [{}]".format(e))
                
def removeDupRedirects(path: str):
    '''
    Removes duplicate sites in redirects.txt
    '''
    sRedirects = []
    uRedirects = []
    try:
        with open(path, "r") as r:
            redirects = r.read().splitlines()
            for redirect in redirects:
                if "scan_aborted" in redirect:
                    continue
                sRedirect = redirect.split("/", 3)
                jRedirect = "//".join([sRedirect[0], sRedirect[2]])
                sRedirects.append(jRedirect)
        for s in sRedirects:
            if s not in uRedirects:
                uRedirects.append(s)
        with open(path, "w") as f:
            for u in uRedirects:
                f.write("%s\n" %u)
        return uRedirects
    except Exception as e:
        logging.error("***database commands*** removeDupRedirects: [{}]".format(e))
        
def join_splits(join_list: list):
    '''
    Joins list to a string with a . delimiter and formats it with a / at the end
    '''
    try:
        joined_split = ".".join(join_list)
        formatted_joined_split = "{}/".format(joined_split)
        return formatted_joined_split
    except Exception as e:
        logging.error("***database commands*** join_splits: [{}]".format(e))
        
def check_sites_in_sites(_site, sites):
    '''
    checks if string is in list
    returns boolean
    '''
    try:
        if _site not in sites:
            return False
        else:
            return True
    except Exception as e:
        logging.error("***database commands*** check_sites_in_sites: [{}]".format(e))
        
def cleanWpscanData(baseDir: str, path: str):
    '''
    Removes duplicate wpscan sites
    '''
    try:
        total_tries = 4
        count = 1
        dirList = os.listdir(baseDir)
        with open(path, "r") as s:
            sites = s.read().splitlines()
            for f in dirList:
                sFile = re.split("_|\\.", f)
                _split = "://".join([sFile[0], sFile[1]])
                join_list = [_split]
                count = 1
                for tries in range(total_tries):
                    count += 1
                    try:
                        join_list.append(sFile[count])
                        _site = join_splits(join_list)
                        result = check_sites_in_sites(_site, sites)
                        if result == False:
                            continue
                        else:
                            count = 1
                            break
                    except:
                        logging.info("Removing {}".format(f))
                        try:
                            count = 1
                            os.remove("{}/{}".format(baseDir, f))
                            break
                        except:
                            continue
    except Exception as e:
        logging.error("***database commands*** cleanWpscanData: [{}]".format(e))
        

    
                
                