from .wpdb import engine
from sqlalchemy import inspect
import pandas as pd
import datetime
import settings
import os
import logging
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
            
def export_table_to_excel():
    ctx = ClientContext(settings.SHAREPOINT['SITE_URL']).with_credentials(UserCredential(settings.SHAREPOINT['USERNAME'], settings.SHAREPOINT['PASS']))
    today = datetime.date.today()
    formatted_date = today.strftime("%-m-%-d-%y")
    reports_file_path = f"{settings.REPORTS_PATH}/wordpresser_{formatted_date}.xlsx"
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    writer = pd.ExcelWriter(reports_file_path, engine='xlsxwriter')
    for table_name in table_names:
        if 'wordpress' in table_name:
            df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
            df.to_excel(writer, sheet_name=table_name, index=False)
    writer.close()
    with open(reports_file_path, "rb") as local_file:
        target_folder = ctx.web.get_folder_by_server_relative_url(settings.SHAREPOINT['FOLDER_PATH'])
        target_folder.upload_file(os.path.basename(reports_file_path), local_file)
        ctx.execute_query()
        logging.info(f"File {reports_file_path} uploaded to SharePoint folder: {settings.SHAREPOINT['FOLDER_PATH']}")
