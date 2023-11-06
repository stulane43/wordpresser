import concurrent.futures
import csv
import json
import logging
import subprocess

import settings

class Pantheon():
    
    def __init__(self) -> None:
        self.domain_list = []
        self.domain_dict = {}
        self.plugin_dict = {}
    
    def query_sites(self):
        '''
        Runs Terminus CLI to query all sites from the Penguin Random House Organization in Pantheon
        - Returns list of sites
        '''
        logging.debug("Getting list of Pantheon sites...")
        output_bytes = subprocess.check_output(settings.PANTHEON['TERMINUS']['query_sites'], shell=True)
        output_str = output_bytes.decode('utf-8').strip()
        sites = output_str.split('\n')
        for site in sites:
            if site in settings.PANTHEON['DO_NOT_SCAN_SITE_LIST']:
                sites.remove(site)
        logging.debug("Got list of Pantheon sites!")
        return sites

    def query_domains(self, site: str, env: str):
        '''
        Queries Pantheon domains based on platform environment
        '''
        domain_command = f'terminus domain:list "{site}.{env}" --fields id --format=list'
        wp_version_command = f"terminus wp {site}.{env} -- core version"
        plugin_command = f'terminus wp "{site}.{env}" -- plugin list --format=json'
        output_bytes = subprocess.check_output(domain_command, shell=True)
        output_str = output_bytes.decode('utf-8').strip()
        
        wp_version_output_bytes = subprocess.check_output(wp_version_command, shell=True)
        wp_version = wp_version_output_bytes.decode('utf-8').strip()
        domains = output_str.split('\n')
        for domain in domains:
            self.domain_dict[domain] = {
                'target': f"{site}.{env}", 
                'wp_version': wp_version
            }
        for domain in domains:
            self.domain_list.append(domain)
        plugin_output_bytes = subprocess.check_output(plugin_command, shell=True)
        plugin_output_str = plugin_output_bytes.decode('utf-8').strip()
        plugins_list = plugin_output_str.split('\n')
        for plugins in plugins_list:
            json_list = json.loads(plugins)
        self.plugin_dict[f"{site}.{env}"] = json_list
        
    def thread_terminus_envs(self, site: str):
        '''
        Threads terminus cli to get faster results
        - Threads dev/test/live environment calls
        '''
        envs = ["live", "test", "dev"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(self.query_domains, [site]*len(envs), envs)

    def thread_terminus_sites(self, sites: list):
        '''
        Threads terminus cli to get faster results
        - Threads list of sites
        '''
        logging.debug("Threading Terminus...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=settings.PANTHEON['MAX_WORKERS']) as executor:
            executor.map(self.thread_terminus_envs, sites)

    def run_terminus(self):
        '''
        Runs Terminus (Pantheon Command Line Tool) to query domains/plugins from the Penguin Random House Organization in Pantheon
        - outputs domains to pantheon.out
        - outputs plugins to pantheon_plugins.csv
        '''
        logging.debug("Gathering domains and plugins from Pantheon...")
        sites = self.query_sites()
        self.thread_terminus_sites(sites)
        with open(settings.PANTHEON['DOMAIN_LIST_OUTPUT_FILE_PATH'], 'w') as f1:
            for domain in self.domain_list:
                f1.write(domain + '\n')
        with open(settings.PANTHEON['DOMAIN_OUTPUT_FILE_PATH'], 'w') as f2:
            json.dump(self.domain_dict, f2, indent=4)
        with open(settings.PANTHEON['PLUGIN_OUTPUT_FILE_PATH'], 'w') as f3:
            writer = csv.writer(f3)
            writer.writerow(['Site', 'Plugin', 'Version'])
            for key, value in self.plugin_dict.items():
                for item in value:
                    plugin = item.get('name', '')
                    version = item.get('version', '')
                    writer.writerow([key, plugin, version])
        logging.debug("Pantheon/Terminus Finished!")
        
        
        