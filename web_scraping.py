
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Web_scraping (): 
    """ 
    Get conact emails of trukers in page https://www.loadmatch.com/login.cfm
    """

    def __init__ (self, userPage, passPage, city_name): 

        # user crdentials of the page
        self.__userPage = userPage
        self.__passPage = passPage

        self.city_name = city_name

        # Pages of the website
        self.__main_page = 'https://www.drayage.com/directory/city.cfm'
        self.__login_page = "https://www.loadmatch.com/login.cfm"

        # Web browser element (google chrome)
        self.__browser = webdriver.Chrome()

        # List of url for each detal to contact a trucker
        self.detail_pages_url = []
        
    def __login (self):
        """
        Open web browser and login to the web page"
        """

        # Open login page in google chrome browser
        self.__browser.get (self.__login_page)


        # Input text of the user credential
        userInput = self.__browser.find_element_by_css_selector ('[name="contact_username"]')

        # Write the user in the input text
        userInput.send_keys(self.__userPage)

        # Input text of the password
        passInput = self.__browser.find_element_by_css_selector ('[name="contact_password"]')

        # Write the password
        passInput.send_keys(self.__passPage)


        # Login button
        loginButton = self.__browser.find_element_by_css_selector ('[name="login_user"]')
        
        # Send click to login button
        loginButton.click() 
    
    def __load_city (self): 
        """
        Load specific city of the main page
        """

        # Load pages of cities
        self.__browser.get (self.__main_page)


        # Css selector of link elements in the web page
        selector = "#bodyWrap > table:nth-child(3) a"
        
        # get all links of the cities in the page
        cities = self.__browser.find_elements_by_css_selector (selector)

        # variable to save the correct link of the city
        city_page = ""

        # loop for each city in the web page
        for city in cities: 
            
            # Save the matching city
            if str(city.text).lower().strip() == str(self.city_name).lower().strip(): 
                city_page = city.get_attribute ("href")
        
        self.__browser.get (city_page)

    def __get_details_pages (self): 
        """
        Get all contact page of each trucker in the current city
        """

        # Css selector of all links in the main table
        selector = "body > table > tbody > tr > td > table:nth-child(1) a"
        selector_company = "body > table > tbody > tr > td > table:nth-child(1) > tbody > tr:nth-child > td:nth-child(14)"

        # Get all links in the main table 
        links_elements = self.__browser.find_elements_by_css_selector (selector)

        # Loop for each link
        for link_element in links_elements: 

            # Verify if link is a detail page
            if str(link_element.text).lower().strip() == "detail": 

                # Save the link in a variable
                url = link_element.get_attribute ("href")

                # Get the position of the parentesis
                start_url_position = str(url).find ("(")
                end_url_position = str(url).rfind (")")

                # Remove aditional text of link
                url = url[start_url_position + 2 :end_url_position - 1]

                # Add link to list of pages
                self.detail_pages_url.append (url)     

    def get_email_truckers (self): 
        """
        Return a list of contact emails of a possible truckers
        """        

        # Makle a login for the web page
        self.__login()

        # Go to page of specific city
        self.__load_city()

        # Get all of details utl pages
        self.__get_details_pages ()

        # variable top save the contact emails
        emails = []

        # Loop for each page in details pages
        for page in self.detail_pages_url:

            self.__browser.get (page)

            # CSS selecor for link emails
            selector = "a"

            # Get posible emails elements
            links_elements = self.__browser.find_elements_by_css_selector (selector)

            # Loop for each posible email
            for link_element in links_elements: 

                # Verify if link is an email
                if "@" in link_element.text: 

                    # Verity that the current email is not in the list of emails
                    if link_element.text not in emails: 

                        # Add email to email list
                        emails.append (link_element.text)

        self.__browser.close()
        return emails




