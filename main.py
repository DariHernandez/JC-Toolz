#! python3
# Enviar un correo electrónico personalizado para una solicitud de trabajo a los camioneros, en base a la información obtenida a través de un formulario web

import os, pprint
from google_sheets import Google_sheets
from email_manager import Email_manager
from data_manager import Data_manager

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


    my_email.send_email (to_email = "hernandezdarifrancisco@gmail.com", subject = "Example email", text = "This is a text email")


# Web sraping for page

    # Open eachpage of Potential truckers

    # Get email of each trucker

    # Send each email with current user account



