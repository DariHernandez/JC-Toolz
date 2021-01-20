#! python3
# Manage email account to send emails

import smtplib, logging, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email_manager ():
    def __init__ (self, email_server, password_server):
        """
        Constructor of the class. Create variables of the instance
        """

        self.email_server = email_server
        self.password_server = password_server

        # Loggin to the email server account, and get the server smtp object
        self.smtpObj_server = self.login (email_server, password_server)
        

    def __get_smtp (self):

        # Return the correct smtp for each email client

        # Dicionary of email provider
        email_provider =  {
            "gmail.com": "smtp.gmail.com", 
            "yahoo.com": "smtp.mail.yahoo.com", 
            "outlook.com": "smtp.office365.com", 
            "hotmail.com": "smtp.office365.com", 
            "aol.com": "smtp.aol.com"
        }

        # Loop for each email provider in the list
        for provider_name, provider_smtp in email_provider.items(): 
            
            # use the smtp server that corresponds to the mail used by the user
            if self.email_user.endswith (provider_name):
                self.smtp = provider_smtp

    
    def login (self, email_user, password_user):  
        """
        Login to smtp account
        """

        # Variables of class 
        self.email_user = email_user
        self.password_user = password_user
        self.smtp = ""
        self.port = "587"
        self.smtpObj = None

        # Get smtp server for the user email account
        self.__get_smtp()

        # User empty smtp object
        self.smtpObj_client = None

        # get SMTP object
        try: 
            # Try to connect with smtp service
            smtpObj = smtplib.SMTP(self.smtp, self.port)
            
            # Send a "hello" to smtp service to verify that everything os okey
            smtpObj.ehlo()

            # Start security protocol
            smtpObj.starttls()
        except:            
            menssage = "Error to login: SMTP( {} ) or SMTP Port ( {} ) error".format(self.smtp, self.port)

            # Send email to user with error information, with server email
            self.smtpObj_server.sendmail(self.email_server, self.email_user, "Subject: Error to login JC Toolz\n\n"+menssage+"\n NO REPLAY")

            # Raise an error to stop program
            raise ValueError (menssage)
        else: 
            # If no error happends...

            try:
                # Try to loggin with user and password_user, with server email
                smtpObj.login(self.email_user, self.password_user)
                
                # Save the smtp object with the client account
                self.smtpObj_client = smtpObj

                # return the smtp object with the mail session already started
                return smtpObj

            except: 
                menssage = 'Error to login: Email adrress ( {} ) of password_user ( {} ) error.'.format (self.email_user, self.password_user)

                # Send email to user with error information
                self.smtpObj_server.sendmail(self.email_server, self.email_user, "Subject: Error to login JC Toolz\n\n"+menssage+"\n NO REPLAY") 

                # If error happends while loggin, then raise an error to stop program
                raise ValueError (menssage)

    def send_email (self, to_email, subject, text): 
        """ 
        Send email to especific reciever 
        """

        # Crate the message with the structure: subject, double line breack and text of the email
        message = "Subject: {} \n\n {}".format (subject, text)

        # Send message
        self.smtpObj_client.sendmail (self.email_user, to_email, message)


