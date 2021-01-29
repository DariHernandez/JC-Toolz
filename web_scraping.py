#! python3

import pprint
import requests, random, bs4, time
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

        # List of proxy servers, to scrape all the information.
        self.proxy_list = [
            "104.248.123.76:18080",
            "206.176.80.60:3128",
            "192.241.218.202:5555",
            "64.235.204.107:3128",
            "185.198.188.54:8080",
            "185.198.188.49:8080",
            "176.9.85.13:3128",
            "217.6.21.170:8080",
            "217.6.21.174:8080",
            "51.158.123.35:9999",
            "51.158.68.68:8811",
            "51.158.68.133:8811",
            "198.50.163.192:3129",
            "51.158.99.51:8811",
        ]

        self.proxy_list_last = []

        # Variable for save all company contact information
        self.contact_data = []
        
        
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



            # Hotfix urls
            url_port_page_end = url_port_page.rfind("port=y")
            url_rail_page_end = url_rail_page.rfind("rail=y")
            url_port_page = url_port_page[:url_port_page_end+6]
            url_rail_page = url_rail_page[:url_rail_page_end+6]

            # get the contact page for each trucker in port and rail transport
            print ("Scraping detail pages of the city...")
            self.__get_details_pages (url_port_page)
            self.__get_details_pages (url_rail_page)

        except: 

            # Reload the same page
            self.__get_details_pages (self.state_city_name_link)

        # Close web browser
        self.browser.close()

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

            # Variable to save the initial row of the table
            initial_row = 3

            # Get the initial row
            selector_first_row = "body > table > tbody > tr > td > table:nth-child(1) > tbody > tr:nth-child(3) > td:nth-child(1)"
            elem_first_row = self.browser.find_element_by_css_selector (selector_first_row)
            colspan_first_row = elem_first_row.get_attribute ("colspan")

            # Update initial row
            if str(colspan_first_row) == "13": 
                initial_row = 4

            # Generate a CSS selector for get all links for each row
            selector_link = "body > table > tbody > tr > td > table:nth-child(1) > tbody > tr:nth-child({}) > td:nth-child(13) > a".format (row_index+initial_row)

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

    def open_proxy_chrome (self):
        """
        Create a google chrome instance with random proxy
        """

        # If instance of web browser if open, close it
        try: 
            self.browser.close()
        except: 
            pass

        # Try to load pages with random proxy
        # If select proxy fail, try with other
        try: 

            # Loop for select new proxy without repetitions 
            while True: 

                # Selecn random proxy
                self.random_proxy = random.choice (self.proxy_list)

                # Verify if proxy exist in the list of last proxies
                if self.random_proxy in self.proxy_list_last:

                    # If all proxies has been used, allow repetitions 
                    if len(self.proxy_list_last) != len (self.proxy_list): 
                        break
                
                # if proxy is not in last list, accept it and add to list
                else: 
                    self.proxy_list_last.append (self.random_proxy)
                    break

            # Configure chrome with the random proxy
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server={}'.format(self.random_proxy))

            #  Make a new web browser with proxy configurations
            self.browser = webdriver.Chrome(options=chrome_options)     

            # Make login to preview information
            self.login()
        
        # Catch error and try again with recursivity
        except: 
            self.browser.close()
            return self.get_contact_data()


    def get_contact_data (self): 
        """
        Return a list of contact emails of a possible truckers
        """        

        # Loop for each page in details pages
        for company_name,page  in self.detail_pages_url:

            # variable top save the contact emails in each page
            emails = []

            # List data pages for the company
            web_pages = [page]

            # Loop to open the current page
            while True: 

                # Try to open page. If error happend, reload chrome with other proxy
                try: 
                    # Open the details page
                    self.browser.get (page)     

                    # Verify if page have not an error to load: Get header of the table
                    elem_table_header = self.browser.find_element_by_css_selector ("body > table:nth-child(2) > tbody > tr:nth-child(1) > td")
                except: 
                    # Reload chrome
                    self.open_proxy_chrome()
                else: 
                    break


            # GET EMAILS

            # CSS selecor for link emails
            # selector = "body > table:nth-child(2) > tbody > tr:nth-child(7) > td:nth-child(2) > a > u"
            selector = "a > u"

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
            

            # Control variable to detect if current register already exist in the list
            current_register_in_list = False

            # If contact data list isn't empty, validate each value
            if self.contact_data: 

                # read all register for the contact data
                for contact_row in self.contact_data: 

                    # Get the company name, emails and web page fo the current register
                    row_name = contact_row["company_name"]
                    row_emails = contact_row["emails"]

                    # Verify if the company already exist in the contact data
                    if row_name == str(company_name).strip(): 
                        
                        # Update control variable
                        current_register_in_list = True

                        # Loop for each email in new email list
                        for email in emails: 
                            
                            # If email no current email do no exist in the last email list, add it
                            if not email in row_emails: 
                                row_emails.append (email)

                        # Add the update data to contact list
                        contact_row["emails"] = row_emails
                    
            
            # Verify if the current register is a new register
            if not current_register_in_list: 

                # Save new register in contact list, ad a dictionary
                self.contact_data.append ({
                    "company_name": str(company_name).strip(), 
                    "emails": emails, 
                    "web_page": self.__short_url(page)
                    })

        # Close current browser
        self.browser.close()

        return self.contact_data

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


my_web_scraping.login()
my_web_scraping.load_city()
my_web_scraping.load_port_rail_pages()
contact_data = my_web_scraping.get_contact_data()
pprint.pprint (contact_data)