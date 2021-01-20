#! python3
# Enviar un correo electrónico personalizado para una solicitud de trabajo a los camioneros, en base a la información obtenida a través de un formulario web

import os, pprint
from google_sheets import Google_sheets
from email_manager import Email_manager
from data_manager import Data_manager
from web_scraping import Web_scraping

# TODO Test mode

# Link of the google sheet
sheet = "https://docs.google.com/spreadsheets/d/1ecgbu4-tBPrXJtZzMFKN1YQdBdJ9aE5tKWLGBdDhVE0/edit?usp=sharing"

# Instance ofg the google sheedt class
my_sheet = Google_sheets (sheet)

# Save the list of google sheet data
data = my_sheet.get_data()



# Path of the project
current_path = os.path.dirname (__file__)

# Path of the csv file with local data
csv_file_path = os.path.join (current_path, "data.csv")

# Instance of the data manager class
my_data_manager = Data_manager (csv_file_path)

# Compare the local data and the new data. return new registers
new_data = my_data_manager.compare_data (data)

# Loop for each new register of data
for row in new_data: 

    # EMAIL CONECTION

    # Local email account to send error message
    email_server = "lbexpressinvoices@gmail.com"
    password_server = "Superman2019"

    # Email information of the client
    email_user = row["email"]
    password_user = row["pass"]

    # Make an instance of the email manager
    my_email = Email_manager (email_server, password_server)

    # Do a login to smtp service
    my_email.login (email_user, password_user)


    # WEB SCRAPING

    # name of the city to make web sraping
    city_name = row["city"]
    
    # Credentials of the web page
    page_user = "kyitzchok"
    page_password = "freightNY"

    # Instance of the web scraping class
    my_web_scraping = Web_scraping (page_user, page_password, city_name)
    emails = my_web_scraping.get_email_truckers ()

    # Make a loop for each contact email
    for email in emails: 
        
        # get data for the email from google sheet
        amount = row["amount"]
        type_container = row["type"]
        overweight = row["overweight"]
        commodity = row["commodity"]
        pick = row["pick"]
        drop = row["drop"]
        cut = row["cut"]
        erd = row["erd"]
        city = row["city"]

        # Structure Email with user data input

        # Add variables to subject
        subject_mail = "[EXTERNAL] Freighters dray request {} to {}".format (pick, drop)

        # Add variables to text 
        text_mail = ""
        text_mail += "Please let us know if you have capacity to carry this this week"
        text_mail += "\n\nThe rail cut off is {}".format(cut)
        text_mail += "\n\nWe have {} x {}'".format (amount, type_container)
        text_mail += "\nLegal Weight" # PENDIENTE: Overweight shipment?
        text_mail += "\n\n{}.".format (erd)
        text_mail += "\n\nCommodity: {}".format (commodity)
        text_mail += "\n\nPick up empty from {}".format (pick)
        text_mail += "\n\nLoad the containers at {}".format (drop)
        text_mail += "\n\nIf you have the capacity, please advise on the price"

        # Merge subject and text with the necesary structure to send the email
        full_mail = "Subject: " + subject_mail + "\n\n" + text_mail 

        # TODO Send email to each receiver



    




# Web sraping for page

    # Open eachpage of Potential truckers

    # Get email of each trucker

    # Send each email with current user account



