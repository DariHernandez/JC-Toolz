#! python3
# Contect with google sheet and download new data

import gspread, sys
from oauth2client.service_account import ServiceAccountCredentials

class Google_sheets (): 
    """ Class to conect to google shets and upload data"""

    def __init__ (self, google_sheet_link): 
        """ Construtor of the class"""

        # Read credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)

        # Try to open a google sheet
        try: 
            # Conect to google sheet
            sheet = client.open_by_url(google_sheet_link)

            # Set the sheet 1 as worksheet
            self.worksheet = sheet.sheet1

        # If error, return a message end end program
        except Exception as err:
            print ("\nERROR TO OPEN GOOGLE SHEET. CHECK THE LINK AND TRY AGAIN.\n")
            print (err)
            sys.exit()

    def get_data (self): 
        """ Read all records of the sheet"""

        records = self.worksheet.get_all_records()
        return records

