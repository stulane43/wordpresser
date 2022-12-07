import wordpresser

if __name__ == '__main__':
    connector = wordpresser.Connector("wordpresser_scan")
    wordpresser.createTables(False)
    # DONE - 1 Pull latest wordpress_sites data into a dataframe
    # DONE - 2 if a site has been seen in the last 7 days, don't run a scan on it (add it to a list for not running) 
    doNotScanList = wordpresser.runWordPress(connector.details)
    wordpresser.runWmap(connector.details, True)
    wordpresser.runCycognito(connector.details, True)
    wordpresser.runAmass(connector.details, True)
    # # DONE - 1 if the site from terminus is in the "do not scan list", don't look for plugins, skip it
    wordpresser.runTerminus(connector.details, doNotScanList, True)
    # # DONE - 1 if the site in the discovered_hosts list is in the "do not scan list", don't run httprobe on it, skip it 
    wordpresser.runHttprobe(connector.details)
    
    # # Fix redirections 
    # #1 if wpscan site has redirections, have redirection column equal 0
    # DONE - if there is a redirect in wpscan, log that redirect site and then insert that into database
    # DONE - if basic auth is required, find that response in wpscan and add to redirect list for rescanning with basic auth parameters
    
    # # if a site in list of manual sites is not in the "do not scan list", run new wpscan on that site
    wordpresser.runWpscan(connector.details, dbInsert=True, discScan=True)
    wordpresser.callStoredProcs()
    wordpresser.runAlerts(connector.details)
    
    # pull all plugins from terminus_plugins and wpscan_plugins and add to a unique dictionary with key:value pairs (site:plugin)
    # Run vuln scan on each unique plugin
    # output data to plugin into plugin_vulns table
    # alert sites using vulnerable plugins
    
    # Repeat for themes
    
    # Repeat for wordpress version