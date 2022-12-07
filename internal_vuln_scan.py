import wordpresser

if __name__ == '__main__':
    connector = wordpresser.Connector("wordpresser_scan")
    wordpresser.createTables(False)
    wordpresser.runWpscan(connector.details, dbInsert=True, discScan=True, manualScan=True)