import gspread

def initGspreadClient(token):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "tokens/{}.json".format(token), scope)
    client = gspread.authorize(creds)
    return clien