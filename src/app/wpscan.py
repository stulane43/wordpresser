import pandas as pd

import settings
import utils

import csv
import json
import logging
import requests
import time

from packaging.version import Version

def plugin_scan():
    logging.debug("Starting plugin scan...")
    api_keys = settings.WPSCAN['API_KEY_LIST']
    api_key_index = 0
    api_count = 0
    
    pantheon_plugins = pd.read_csv(settings.PANTHEON['PLUGIN_OUTPUT_FILE_PATH']).drop_duplicates().reset_index(drop=True)
    # combined_plugins_df = utils.file_utils.combine_two_csv_files(file1=settings.PANTHEON['PLUGIN_OUTPUT_FILE_PATH'], file2=settings.WPSCAN['PLUGIN_OUTPUT_FILE_PATH'])
    pantheon_plugins.to_csv(settings.WPSCAN['PANTHEON_PLUGIN_OUTPUT_FILE_PATH'])
    with open(settings.WPSCAN['PANTHEON_PLUGIN_OUTPUT_FILE_PATH'], 'r') as file, open(settings.WPSCAN['PLUGIN_VULN_OUTPUT_FILE_PATH'], 'w', newline='') as output_file:
        reader = csv.DictReader(file)
        writer = csv.writer(output_file)
        writer.writerow(settings.WPSCAN['PLUGIN_VULN_HEADERS'])
        plugins = set()
        with open(settings.WPSCAN['PLUGINS_NOT_FOUND_FILE_PATH'], 'a+') as not_found_file:
            not_found_file.seek(0)
            not_found = not_found_file.read().splitlines()
        for row in reader:
            plugins.add(row['Plugin'])
        sorted_plugins = sorted(plugins)
        for plugin in sorted_plugins:
            if plugin in not_found:
                logging.debug(f'Skipping {plugin} - Not in WPScan Database...')
                continue
            api_count += 1
            if api_count == 74:
                api_key_index = (api_key_index + 1) % len(api_keys)
                logging.debug(f'API limit reached, switching to API key {api_key_index + 1}')
                api_count = 0
            endpoint = f'{settings.WPSCAN["WPSCAN_PLUGIN_ENDPOINT"]}/{plugin}'
            headers = {'Authorization': f'Token token={api_keys[api_key_index]}'}
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200:
                response_json = json.loads(response.content)
                if 'vulnerabilities' in response_json[plugin]:
                    vulnerabilities = response_json[plugin]['vulnerabilities']
                    if len(vulnerabilities) > 0:
                        for vulnerability in vulnerabilities:
                            fixed_in_version = vulnerability['fixed_in']
                            if fixed_in_version is not None:
                                file.seek(0)
                                for row in reader:
                                    if row['Plugin'] == plugin:
                                        try:
                                            if Version(row['Version']) < Version(fixed_in_version):
                                                writer.writerow([row['Site'], row['Plugin'], row['Version'], fixed_in_version, vulnerability['title']])
                                                logging.info(f'Alert: {row["Site"]} - {row["Plugin"]} {row["Version"]} is vulnerable to Plugin: {plugin} Vulnerability: {vulnerability["title"]} (fixed in {fixed_in_version})')
                                        except Exception as e:
                                            pass
                            elif row['Plugin'] == plugin:
                                writer.writerow([row['Site'], plugin, row['Version'], '', vulnerability['title'] + ' (no fix version specified)'])
                                logging.info(f'Warning: {plugin} {row["Version"]} may be vulnerable to {vulnerability["title"]} (no fix version specified)')
                            else:
                                continue
                else:
                    logging.info(f'{plugin} has no vulnerabilities')
            elif response.status_code == 404:
                with open(settings.WPSCAN['PLUGINS_NOT_FOUND_FILE_PATH'], 'a+') as not_found_file:
                    not_found.append(plugin)
                    not_found_file.write(plugin + '\n')
                logging.debug(f'Plugin {plugin} not found')
            elif response.status_code == 429:
                api_key_index = (api_key_index + 1) % len(api_keys)
                logging.error(f'API limit reached, switching to API key {api_key_index + 1}')
                time.sleep(5)
            else:
                print(f'Error {response.status_code} while retrieving {plugin}')
    logging.info("Plugin Vulnerability Scan Completed!")