#! python3

import os, random

class Template_emails (): 
    """
    Manage and return the templates for the email message
    """

    def __init__ (self, data): 
        """ 
        Cunstructor of the class
        """

        # make variables of class from variables of the current data row 
        self.amount = data["amount"]
        self.type_container = data["type"]
        self.weight = data ["weight"]
        self.overweight = data["overweight"]
        self.commodity = data["commodity"]
        self.pick = data["pick"]
        self.loading = data["loading"]
        self.drop = data["drop"]
        self.cut = data["cut"]
        self.erd = data["erd"]
        self.aditional = data ["aditional"]

        # Path of the project
        current_path = os.path.dirname (__file__)

        # Path of Email templates folder
        self.templates_folder = os.path.join (current_path, "template_emails")

        self.__validate_variables ()


    def __validate_variables (self): 
        """
        Modify the values of the variables that need to be omitted 
        or that need additional information
        """

        # If variable isn't empty, add the complementary information
        if str(self.weight).lower().strip() != "": 
            self.weight = "Approximate Weight: " + str(self.weight) + "kgs"

        # If variable is "yes" Convert to text. Else, set to empty
        if str(self.overweight).lower().strip() == "yes": 
            self.overweight = "Overweight shipment"
        else: 
            self.overweight = ""

        # If loading is empty, replice as back character 
        if str(self.loading).lower().strip() == "": 
            self.loading = ""



    def get_email_text (self, template_num): 
        """
        Return text message with specific number of template
        """
    
        # Generate the path of the selected file 
        path_file = os.path.join(self.templates_folder, str(template_num))

        # Open text file in read mode
        file_reader = open (path_file, "r")

        # Get in a list, all lines of the texst file
        text_lines = file_reader.read()

        # replice the variables in the message template
        text_lines = text_lines.replace ("<amount>", str(self.amount))
        text_lines = text_lines.replace ("<type_container>", str(self.type_container))
        text_lines = text_lines.replace ("<weight>", str(self.weight))
        text_lines = text_lines.replace ("<overweight>", str(self.overweight))
        text_lines = text_lines.replace ("<commodity>", str(self.commodity))
        text_lines = text_lines.replace ("<pick>", str(self.pick))
        text_lines = text_lines.replace ("<loading>", str(self.loading))
        text_lines = text_lines.replace ("<drop>", str(self.drop))
        text_lines = text_lines.replace ("<cut>", str(self.cut))
        text_lines = text_lines.replace ("<erd>", str(self.erd))
        text_lines = text_lines.replace ("<aditional>", str(self.aditional))

        # Separate the emails in parts
        email_subject = ""
        email_body = ""

        # Remove empty lines and add line breaks
        for line in str(text_lines).split('\n'):

            # Skip empty lines
            if line != "": 
            
                # Save the first line in the subject var
                if email_subject == "": 
                    email_subject = line

                # Add the other lines to the body var
                else: 
                    email_body += line + "\n\n"

        # Create the correct structure to send the email with smtl service
        message = "Subject: " + email_subject + "\n\n" + email_body 

        return message

    def get_email_text_random (self): 
        """
        Get the email text with random template
        """

        # Get a list of files in the templates folder
        files = os.listdir (self.templates_folder)

        # Get a random file with the files list
        file_random = random.choice (files)

        # Get the message with the random template
        message = self.get_email_text (file_random)

        return message