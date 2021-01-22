#! python3

import pprint
import requests, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Web_scraping (): 
    """ 
    Get conact emails of trukers in page https://www.loadmatch.com/login.cfm
    """

    def __init__ (self, userPage, passPage, state_name, city_name, port_rail): 

        # user crdentials of the page
        self.userPage = userPage
        self.passPage = passPage

        # Variables for the web scraping
        self.state_name = state_name
        self.city_name = city_name
        self.state_city_name = self.state_name + " - " + self.city_name
        self.state_city_name_link = ""
        self.port_rail = port_rail

        # Pages of the website
        self.main_page = 'https://www.drayage.com/directory/city.cfm'
        self.login_page = "https://www.loadmatch.com/login.cfm"

        # Web browser element (google chrome)
        self.browser = webdriver.Chrome()

        # List of url for each detal to contact a trucker
        self.detail_pages_url = []
        
    def login (self):
        """
        Open web browser and login to the web page"
        """

        # Open login page in google chrome browser
        self.browser.get (self.login_page)


        # Input text of the user credential
        userInput = self.browser.find_element_by_css_selector ('[name="contact_username"]')

        # Write the user in the input text
        userInput.send_keys(self.userPage)

        # Input text of the password
        passInput = self.browser.find_element_by_css_selector ('[name="contact_password"]')

        # Write the password
        passInput.send_keys(self.passPage)


        # Login button
        loginButton = self.browser.find_element_by_css_selector ('[name="login_user"]')
        
        # Send click to login button
        loginButton.click() 

    def __generate_city_page (self): 
        """
        Save as class var the link of the correct city page
        """

        # Css selector of link elements in the web page
        selector = "#bodyWrap > table:nth-child(3) a"

        # get all links of the cities in the page
        cities = self.browser.find_elements_by_css_selector (selector)

        # variable to save the correct link of the city
        city_page = ""

        # loop for each city in the web page
        for city in cities: 
            
            # Save the matching city
            if str(city.text).lower().strip() == str(self.state_city_name).lower().strip(): 
                city_page = city.get_attribute ("href")
        
        self.state_city_name_link = city_page
    
    def load_city (self): 
        """
        Load specific city of the main page
        """

        # Load pages of cities
        self.browser.get (self.main_page)

        # Generate the link of the current city page
        self.__generate_city_page()

        #  Open link of the correct city
        self.browser.get (self.state_city_name_link)


    def load_port_rail_pages (self):
        """
        Detect pages who need to port or rail option, and load it. 
        Other else, directly load
        """ 

        selector_port = "body > table > tbody > tr > td > table:nth-child(1) > tbody > tr:nth-child(3) > td.midblack > a:nth-child(2)"
        selector_rail = "body > table > tbody > tr > td > table:nth-child(1) > tbody > tr:nth-child(3) > td.midblack > a:nth-child(4)"

        # Try to select port and rail links. 
        # If no error happend, load each page: page to port transport and page to rail transport
        # Else catch the error and no reload the page
        try: 

            # Get links
            link_port = self.browser.find_element_by_css_selector (selector_port)
            link_rail = self.browser.find_element_by_css_selector (selector_rail)

            # get the url to pages with data filtered
            url_port_page = link_port.get_attribute("href")
            url_rail_page = link_rail.get_attribute("href")

            # get the contact page for each trucker in port and rail transport
            self.__get_details_pages (url_port_page)
            self.__get_details_pages (url_rail_page)

        except: 

            # Reload the same page
            self.__get_details_pages (self.state_city_name_link)



    def __get_details_pages (self, page): 
        """
        Get all contact page of each trucker in the current city
        """

        self.browser.get (page)

        # Css selectors of company name and transport type
        selector_company = "body > table > tbody > tr > td > table:nth-child(1) > tbody > tr > td:nth-child(14)"
        selector_port_rail = "body > table > tbody > tr > td > table:nth-child(1) > tbody > tr > td:nth-child(4)"

        # Get all names of companies in tha main table
        name_elements = self.browser.find_elements_by_css_selector (selector_company)

        # Get all type of transport in the main table
        port_rail_elements = self.browser.find_elements_by_css_selector (selector_port_rail)

        # List of row with the correct value of Port and Rail
        filtered_rows = [] 


        # Loop for each element in the table
        for name_element in name_elements: 
            
            # Get the current number position in the list
            index = name_elements.index (name_element)

            # Empty list to manage the type of transport
            current_port_rail = ""

            # Verify the user input of typo of transport
            if self.port_rail == "port": 

                # Save only the row with post transport
                if "Port" in port_rail_elements[index].text: 
                    filtered_rows.append (index)


            elif self.port_rail == "rail": 

                # Save only the row with rail transport
                if "Rail" in port_rail_elements[index].text: 
                    filtered_rows.append (index)


            elif self.port_rail == "both": 

                # Save all rows
                filtered_rows.append (index)

        # make a loop for each valid row in the main table
        for row_index in filtered_rows: 

            #  List of links for each row
            urls = []

            # get the name of the current company
            company_name = name_elements[row_index].text

            # Generate a CSS selector for get all links for each row
            selector_link = "body > table > tbody > tr > td > table:nth-child(1) > tbody > tr:nth-child({}) > td:nth-child(13) > a".format (row_index+3)

            # Try to get element of details
            try: 
                # If element exist / no error happend, save it

                # Get the link elements from the web page
                link_element = self.browser.find_element_by_css_selector (selector_link)

                # Get the url of each link
                url = link_element.get_attribute ("href")

                # Get the position of the parentesis
                start_url_position = str(url).find ("(")
                end_url_position = str(url).rfind (")")

                # Remove aditional text of link
                url = url[start_url_position + 2 :end_url_position - 1]

                
                # Save each link of links in the dicationary. 
                # The key is the name of the company, and the value is a list of links
                self.detail_pages_url.append ((company_name, url))
            except:

                # If element doesnt exist / error happend, continue to the next element
                continue


    def get_contact_data (self): 
        """
        Return a list of contact emails of a possible truckers
        """        

        # Login to the page
        self.login()

        # Load the correct city from the user input
        self.load_city()

        # Filter result between port and rail transport
        self.load_port_rail_pages()

        # Variable for save all company emails
        contact_data = []

        
        # Loop for each page in details pages
        for company_name,page  in self.detail_pages_url:

            # variable top save the contact emails in each page
            emails = []

            # List data pages for the company
            web_pages = [page]
        

            # Open details page
            self.browser.get (page)
            print (company_name)

            # Update the vpn in each query, so as not to saturate the web page servers

            # GET EMAILS

            # CSS selecor for link emails
            selector = "a"

            # Get posible emails elements
            links_elements = self.browser.find_elements_by_css_selector (selector)

            # Loop for each posible email
            for link_element in links_elements: 

                # Verify if link is an email
                if "@" in link_element.text: 

                    # Verity that the current email is not in the list of emails
                    if link_element.text not in emails: 

                        # Add email to email list
                        emails.append (link_element.text)
            

            # read all register for the contact data
            for contact_row in contact_data: 

                # Get the company name, emails and web page fo the current register
                row_name = contact_row["company_name"]
                row_emails = contact_row["emails"]
                row_web_page = contact_row["web_pages"]

                # Verify if the company already exist in the contact data
                if row_name == str(company_name).strip(): 

                    # Loop for each email in new email list
                    for email in emails: 
                        
                        # If email no current email do no exist in the last email list, add it
                        if not email in row_emails: 
                            row_emails.append (email)
                    
                    # Add the new erb page to the last web page list
                    row_web_page.append (self.__short_url(page))

                    # Add the update data to contact list
                    contact_row["emails"] = row_emails
                    contact_row["web_pages"] = row_web_page
                
                # If company doesn't exist in the contact list, add it
                else: 

                    # Save new register in contact list, ad a dictionary
                    contact_data.append ({
                        "company_name": str(company_name).strip(), 
                        "emails": emails, 
                        "web_pages": self.__short_url(page)
                        })

        self.browser.close()
        return contact_data

    def __short_url (self, url): 
        """
        Short url with tinyurl and return shorted link
        """

        # API for short links
        tinyurl_api = "https://tinyurl.com/api-create.php?url={}".format (url)

        # Get the response of the api
        shorted_url = requests.get (tinyurl_api)

        # Return the shorted link
        return shorted_url.text




# my_web_scraping = Web_scraping ("kyitzchok", "freightNY", "AK", "Anchorage", "both")
# my_web_scraping = Web_scraping ("kyitzchok", "freightNY", "AL", "Mobile", "both")
my_web_scraping = Web_scraping ("kyitzchok", "freightNY", "CA", "Los Angeles", "both")
# my_web_scraping = Web_scraping ("kyitzchok", "freightNY", "PA", "Scranton/Taylor", "both")
# my_web_scraping = Web_scraping ("kyitzchok", "freightNY", "SC", "Greer", "both")
# my_web_scraping = Web_scraping ("kyitzchok", "freightNY", "TN", "Memphis", "both")

contact_data = my_web_scraping.get_contact_data()
pprint.pprint (contact_data)