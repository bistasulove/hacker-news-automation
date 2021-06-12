import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
load_dotenv()

def get_sheet():
    # use creds to create a client to interact with the Google Drive API
    scopes = ["https://spreadsheets.google.com/feeds"]
    json_creds = os.environ.get("GOOGLE_SHEETS_CREDS_JSON")

    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    client = gspread.authorize(creds)

    # Find a workbook by url
    spreadsheet = client.open_by_url(os.environ.get('SHEETS_URL'))
    sheet = spreadsheet.sheet1
    return sheet

# Extract and print all of the values
def get_all_records():
    sheet = get_sheet()
    rows = sheet.get_all_records()
    data = []
    for row in rows:
        item = {}
        for key,value in row.items():
            if key.lower() == 'email':
                item[key.lower()] = value.lower()
            elif key.lower() == 'interests':
                item[key.lower()] = value.lower().replace(' ', '').split(',')
        
        data.append(item)
    return data

def add_to_gsheet(email, interests):
    sheet = get_sheet()
    rows = sheet.get_all_records()
    row = [email, interests]
    sheet.insert_row(row, len(rows)+2)

def get_current_index_of_email(email):
    sheet = get_sheet()
    for i in range(2, sheet.row_count + 1):
        row = sheet.row_values(i)
        if row[0] == email.lower():
            return i


def remove_from_gsheet(email):
    sheet = get_sheet()
    index = get_current_index_of_email(email)
    if index:
        sheet.delete_row(index)
        return True
    return False

def check_if_email_present(email):
    data = get_all_records()
    print(data)
    if not any(d['email']==email for d in data):
        return False
    return True
