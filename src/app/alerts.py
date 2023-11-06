import pymsteams
import logging

import database as db
import settings
            
def query(query):
    '''
    looks in wp database and sees if there are any new sites
    '''
    logging.info("Running search...")
    try:
        result = db.commands.read(query)
        result = result.to_dict('records')
        return result
    except Exception as e:
        logging.error("***Alerts*** newSites: [{}]".format(e))
        
def daily_alert():
    card = pymsteams.connectorcard(settings.ALERTS['WEBHOOK'])
    card.text(' ')
    
    # Find New Sites
    newsites = query(settings.ALERTS['query']['NEW_SITES'])
    if newsites != []:
        newsites_section = pymsteams.cardsection()
        newsites_section.title('<h1 style="color:red;">New Site(s) Discovered:</h1>')
        newsites_rows = [
            "| Site Name | Target | WordPress Version | Plugin Count |",
            "| --- | --- | --- | --- |"
        ]
        for site in newsites:
            site_row = f"{site['site']} | {site['target']} | {site['wp_version']} | {str(site['plugins'])}"
            newsites_rows.append(site_row)
        newsites_table = "\n".join(newsites_rows)
        newsites_section.text(newsites_table)
        card.addSection(newsites_section)
        divider_section = pymsteams.cardsection()
        divider_section.text("---")
        card.addSection(divider_section)
    
    # Get Triage Status
    triage_status = query(settings.ALERTS['query']['TRIAGE_STATUS'])
    if triage_status != []:
        triage_section = pymsteams.cardsection()
        triage_section.title('**<h1 style="color:red;">WordPress Vulnerabilities:</h1>**')
        triage_rows = [
            "| To Verify | Confirmed |\n",
            "--- | --- |\n"
        ]
        if len(triage_status) == 1:
            triage_rows.append('0')
        for status in triage_status:
            status_row = f"{status['count']}"
            triage_rows.append(status_row)
        triage_table = " | ".join(triage_rows)
        triage_section.text(triage_table)
        card.addSection(triage_section)
        divider_section = pymsteams.cardsection()
        divider_section.text("---")
        card.addSection(divider_section)

    # Organize Confirmed Risk
    confirmed_risk = query(settings.ALERTS['query']['CONFIRMED_RISK'])
    if confirmed_risk != []:
        risk_section = pymsteams.cardsection()
        risk_section.title('**<h1 style="color:red;">Confirmed Vulnerabilities:</h1>**')
        risk_rows = [
            "| Critical | High | Medium | Low | Total |\n",
            "--- | --- | --- | --- |\n"
        ]
        for risk in confirmed_risk:
            risk_row = f"{int(risk['Critical Risk'])} | {int(risk['High Risk'])} | {int(risk['Medium Risk'])} | {int(risk['Low Risk'])} | {int(risk['Total Vulnerability Count'])}"
            risk_rows.append(risk_row)
        risk_table = " | ".join(risk_rows)
        risk_section.text(risk_table)
        card.addSection(risk_section)
        divider_section = pymsteams.cardsection()
        divider_section.text("---")
        card.addSection(divider_section)
        
    # Get Riskiest Sites
    vulnsites = query(settings.ALERTS['query']['TOP_10_VULN_SITES'])
    if vulnsites != []:
        vulnsites_section = pymsteams.cardsection()
        vulnsites_section.title('<h1 style="color:red;">Top 10 Riskiest Sites:</h1>')
        vulnsites_rows = [
            "| Site Name | Target | WordPress Version | Plugin Count | Plugin Vulnerabilities |",
            "| --- | --- | --- | --- | --- |"
        ]
        for vuln in vulnsites:
            vuln_row = f"{vuln['site']} | {vuln['target']} | {vuln['wp_version']} | {str(vuln['plugins'])} | {str(vuln['plugin_vulns'])}"
            vulnsites_rows.append(vuln_row)
        vulnsites_table = "\n".join(vulnsites_rows)
        vulnsites_section.text(vulnsites_table)
        card.addSection(vulnsites_section)
        card.send()