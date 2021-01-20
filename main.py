#! python3
# Enviar un correo electrónico personalizado para una solicitud de trabajo a los camioneros, en base a la información obtenida a través de un formulario web

from google_sheets import Google_sheets
from email_manager import Email_manager

# Extract data from sheet
sheet = "https://docs.google.com/spreadsheets/d/1ecgbu4-tBPrXJtZzMFKN1YQdBdJ9aE5tKWLGBdDhVE0/edit?usp=sharing"
my_sheet = Google_sheets (sheet)
data = my_sheet.get_data()

# Manage new data

    # Read last data in local storage

    # Ignore duplicate data

    # Save new data

    # Create email

# Local email account to send error message
email_server = "lbexpressinvoices@gmail.com"
password_server = "Superman2019"

# Email information of the client
email_user = data["email"]
password_user = data["pass"]

# Login de smtp email
my_email = Email_manager (email_server, password_server)
my_email.login (email_user, password_user)
my_email.send_email (to_email = "hernandezdarifrancisco@gmail.com", subject = "Example email", text = "This is a text email")


# Web sraping for page

    # Open eachpage of Potential truckers

    # Get email of each trucker

    # Send each email with current user account



