import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials as SAC


def save_table(table):
    sheet.sheet1.update([table.columns.values.tolist()] + table.values.tolist())


# service account key file address in JSON
adress = str(input("Enter the address of the service account key file in JSON: "))

# Share spreadsheet with google account
email = str(input("Enter google account address: "))

# Parsing tables from the site
table_from_site = pd.read_html("https://confluence.hflabs.ru/pages/viewpage.action?pageId=1181220999",
                               encoding='utf-8')
# Connect to Google API
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
credentials = SAC.from_json_keyfile_name(adress, scope)
client = gspread.authorize(credentials)

# Create or update table
try:
    sheet = client.open("Parsing")
    table_from_google = pd.DataFrame.from_dict(sheet.get_worksheet(0).get_all_records())
    if not table_from_site[0].equals(table_from_google):
        save_table(table_from_site[0])

except gspread.exceptions.SpreadsheetNotFound:
    sheet = client.create("Parsing")
    save_table(table_from_site[0])
    print('Table created')

else:
    print('The table is up to date"')

finally:
    sheet.share(email, perm_type='user', role='writer')
