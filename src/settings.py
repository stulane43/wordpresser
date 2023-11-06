import os
from pathlib import Path
import dotenv

BASE_DIR = Path(os.path.abspath(__file__)).parents[1]
APP_DIR = f"{BASE_DIR}/src/app"
OUT_PATH = f"{APP_DIR}/out"
CONFIG_PATH = f'{APP_DIR}/config'
REPORTS_PATH = f"{OUT_PATH}/reports"

dotenv.load_dotenv(f'{CONFIG_PATH}/.env')

DATABASE = {
    'server': {
        'HOST': os.environ['SERVER_HOST'],
        'USER': os.environ['SERVER_USER'],
        'PASS': os.environ['SERVER_PASS'],
        'BIND_ADDRESS': os.environ['BIND_ADDRESS'],
        'BIND_PORT': os.environ['BIND_PORT']
    },
    'mysql': {
        'DATABASE': os.environ['DATABASE'],
        'USER': os.environ['DATABASE_USER'],
        'PASS': os.environ['DATABASE_PASS']
    }
}

PANTHEON = {
    'TERMINUS': {
        'query_sites': 'terminus org:site:list "Penguin Random House" --field=name --format=json'
    },
    'DO_NOT_SCAN_SITE_LIST': [
        'knopfdoubleday',
        'theloraxproject'
    ],
    'DOMAIN_OUTPUT_FILE_PATH': 'src/app/out/pantheon_domains.json',
    'DOMAIN_LIST_OUTPUT_FILE_PATH': 'src/app/config/pantheon_domain_list.out',
    'PLUGIN_OUTPUT_FILE_PATH': 'src/app/out/pantheon_plugins.csv',
    'MAX_WORKERS': 20
}

WPSCAN = {
    'PLUGIN_OUTPUT_FILE_PATH': 'src/app/out/wpscan_plugins.csv',
    'MAX_WORKERS': 20,
    'WPSCAN_PLUGIN_ENDPOINT': 'https://wpscan.com/api/v3/plugins',
    'API_KEY_LIST': [
        os.environ['WPSCAN_API_KEY_1'],
        os.environ['WPSCAN_API_KEY_2'],
        os.environ['WPSCAN_API_KEY_3'],
        os.environ['WPSCAN_API_KEY_4'],
        os.environ['WPSCAN_API_KEY_5'],
        os.environ['WPSCAN_API_KEY_6'],
        os.environ['WPSCAN_API_KEY_7'],
        os.environ['WPSCAN_API_KEY_8'],
        os.environ['WPSCAN_API_KEY_9'],
        os.environ['WPSCAN_API_KEY_10'],
        os.environ['WPSCAN_API_KEY_11'],
        os.environ['WPSCAN_API_KEY_12'],
        os.environ['WPSCAN_API_KEY_13'],
        os.environ['WPSCAN_API_KEY_14'],
        os.environ['WPSCAN_API_KEY_15']
    ],
    'PLUGIN_VULN_HEADERS': [
        'Site',
        'Plugin',
        'Version Affected',
        'Version Fixed',
        'Vulnerability'
    ],
    'PANTHEON_PLUGIN_OUTPUT_FILE_PATH': 'src/app/out/plugins.csv',
    'PLUGIN_VULN_OUTPUT_FILE_PATH': 'src/app/out/wpscan_plugin_vulns.csv',
    'PLUGINS_NOT_FOUND_FILE_PATH': 'src/app/config/wpscan_pluginsnotfound.txt'
}

ALERTS = {
    'WEBHOOK': os.environ['TEAMS_WEBHOOK'],
    'query': {
        'TRIAGE_STATUS': 'select triage_status, count(*) as `count` from wordpress_plugin_vulns wpv where triage_status <> "Not Exploitable" and target like "%%.live" and triage_status <> "False Positive" and remediated = 0 group by triage_status desc',
        'NEW_SITES': 'select site, target, wp_version, plugins from wordpress_sites ws where date(first_seen) = curdate() order by first_seen desc',
        'CONFIRMED_RISK': 'SELECT triage_status as `Triage Status`, SUM(CASE WHEN severity = "Critical" THEN 1 ELSE 0 END) AS `Critical Risk`, SUM(CASE WHEN severity = "High" THEN 1 ELSE 0 END) AS `High Risk`, SUM(CASE WHEN severity = "Medium" THEN 1 ELSE 0 END) AS `Medium Risk`, SUM(CASE WHEN severity = "Low" THEN 1 ELSE 0 END) AS `Low Risk`, COUNT(*) AS `Total Vulnerability Count` FROM wordpress_plugin_vulns wpv where triage_status = "Confirmed" and target like "%%.live" and remediated = 0 GROUP BY triage_status;',
        'TOP_10_VULN_SITES': 'select site, target, wp_version, plugins, plugin_vulns from wordpress_sites ws where target like "%%.live" and site like "%%.com" group by target order by plugin_vulns desc limit 10'
    }
}

SHAREPOINT = {
    'USERNAME': os.environ['SHAREPOINT_USERNAME'],
    'PASS': os.environ['SHAREPOINT_PASS'],
    'SITE_URL': os.environ['SHAREPOINT_SITE_URL'],
    'FOLDER_PATH': os.environ['SHAREPOINT_FOLDER_PATH'],
}