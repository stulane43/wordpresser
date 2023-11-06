import pandas as pd

from . import pantheon
from . import wpscan
from . import alerts

import database as db
import json
import logging
import settings
import utils

class Handler():
    
    def __init__(self) -> None:
        db.commands.create_tables(True)
        pass
        
    def pantheon(self):
        logging.info("Pulling all sites from Pantheon...")
        p = pantheon.Pantheon()
        p.run_terminus()
        
    def wordpress_sites_update(self):
        logging.debug("Inserting/Updating WordPress sites into database...")
        wordpresser_sites = json.load(open(settings.PANTHEON['DOMAIN_OUTPUT_FILE_PATH'], 'r'))
        # wordpresser_sites = utils.file_utils.combine_two_json_files(file1=settings.PANTHEON['DOMAIN_OUTPUT_FILE_PATH'], 
                                                                # file2=settings.WPSCAN['DOMAIN_OUTPUT_FILE_PATH'])
        sites_df = pd.DataFrame.from_dict(wordpresser_sites, orient='index', columns=['target', 'wp_version'])
        sites_df['site'] = sites_df.index
        db.commands.temp_insert(table='temp_wordpress_sites', df=sites_df)
        
    def wordpress_plugins_update(self):
        logging.debug("Inserting/Updating WordPress plugins into database...")
        plugins_df = pd.read_csv(settings.PANTHEON['PLUGIN_OUTPUT_FILE_PATH']).drop_duplicates().reset_index(drop=True)
        # plugins_df = utils.file_utils.combine_two_csv_files(file1=settings.PANTHEON['PLUGIN_OUTPUT_FILE_PATH'], 
                                                                # file2=settings.WPSCAN['PLUGIN_OUTPUT_FILE_PATH'])
        db.commands.temp_insert(table='temp_wordpress_plugins', df=plugins_df)
        
    def wpscan_plugin_vuln_scan(self):
        logging.info("Finding Plugin Vulnerabilities with WPScan...")
        wpscan.plugin_scan()
        
    def wordpress_plugin_vulns_update(self):
        logging.debug("Inserting/Updating WordPress Plugin Vulnerabilities into database...")
        vulns_df = pd.read_csv(settings.WPSCAN['PLUGIN_VULN_OUTPUT_FILE_PATH'])
        db.commands.temp_insert(table='temp_wordpress_plugin_vulns', df=vulns_df)
        
    def wordpresser_alerts(self):
        logging.debug("Querying database and sending teams alerts...")
        alerts.daily_alert()
        
    def stored_procs(self):
        logging.debug("Running stored procedures...")
        db.commands.call_stored_procs()
        
    def export_data(self):
        logging.debug("Running export")
        db.export_db.export_table_to_excel()