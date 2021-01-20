
import time, csv, sys, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class WebExtract (): 
    """ Extract order information, from the web store.tcgplayer.com"""

    def __init__ (self, userPage, passPage): 
        print ('Opening Chrome...')

        # user crdentials
        self.__userPage = userPage
        self.__passPage = passPage

        # Web an order
        self.__page = 'https://www.drayage.com/directory/city.cfm'
        self.__orders = []

        # CSv folder
        self.__path = os.path.dirname (__file__)
        self.__csvFolder = os.path.join (self.__path, 'csv')

        self.__browser = webdriver.Chrome()
        
        

    def setOrders (self, orderList): 
        self.__orders = orderList

    def setCsvFile (self,  csvFile): 
        self.__csvFile = csvFile

    def login (self):
        """ Open web browser and login to the web page"""

        # Login
        self.__browser.get (self.__page)
        try: 
            # Wait for load page
            userInput = None
            while not userInput: 
                userInput = self.__browser.find_element_by_css_selector ('[name="contact_username"]')
                userInput.send_keys(self.__userPage)
                passInput = self.__browser.find_element_by_css_selector ('[name="contact_password"]')
                passInput.send_keys(self.__passPage)
                time.sleep(1)

            # Check if login button is active
            loginButton = self.__browser.find_element_by_css_selector ('[name="login_user"]')
            if loginButton.is_enabled(): 
                loginButton.click() 
                print ('Auto login completed')
            else: 
                #Wait to continue or reload the page if the recaptcha fail
                print ('\nPlease manually complete the reCaptchain in  chrome...\n')
                askContinue = input ('Correct login? (y/n) ')
                if askContinue.lower()[0] != 'y':
                    self.__browser.close()
                    self.login ()
        except: 
            askContinue = input ('Correct login? (y/n) ')
            if askContinue.lower()[0] != 'y':
                self.__browser.close()
                self.login ()
            
        
        

    def __saveData (self, names, prices, cuantities, costs, order, outputWriter):
        """ Read exctrated info, and write in a CSV file"""

        for row in range (len(names)): 
            currentRow = []

            # Write order number
            currentRow.append (order)
            

            # # Separate name in columns
            # name_parts = (names[row].text).split(':')
            # for name_part in name_parts: 
            #     str(name_part).index ()
            #     name_sections = name_part.split (' - ')
            #     for names_section in name_sections: 
            #         # Write name columns
            #         currentRow.append(names_section)
            
            currentRow.append((names[row].text)[:(names[row].text).index('-')].strip())
            currentRow.append((names[row].text)[(names[row].text).index('-')+1:(names[row].text).index(':')])
            currentRow.append((names[row].text)[(names[row].text).index(':')+1:(names[row].text).rfind('-')])
            currentRow.append((names[row].text)[(names[row].text).rfind('-')+1:])
            

            # Write last columns
            currentRow.append(float((prices[row].text)[1:]))
            currentRow.append(int(cuantities[row].text))
            currentRow.append(float((costs[row].text)[1:])) 
            
            outputWriter.writerow(currentRow)
            print ('Adding row to %s file' % (self.__csvFile))
    
    def extract (self):
        """Extract infomation from page of each order"""

        # Check if orderas already exist
        if self.__orders:

            # Open file
            csvFile = os.path.join (self.__csvFolder, self.__csvFile)
            outputFile = open(csvFile, 'a', newline='')
            outputWriter = csv.writer(outputFile)

            # Writre header
            outputWriter.writerow(["Order", "Game", "Set", "Card", "Condition", "Price", "Cuantity", "Cost"])
        
            print ('Extracting info...')

            # loop for each order 
            for order in self.__orders:

                # Load order page
                self.__browser.get (self.__page + '/' + order)

                # Selector to find elements in the html page
                names_selector      = 'table > tbody > tr.gradeA > td:nth-child(1) > a'
                prices_selector     = 'table > tbody > tr.gradeA > td:nth-child(2) > div '
                cuantities_selector = 'table > tbody > tr.gradeA > td:nth-child(3) > div'
                costs_selector      = 'table > tbody > tr.gradeA > td:nth-child(4) > div'

                # Exctract information from html elements
                names = None
                print ('Waiting for the page (order: %s)...' % order)
                while not names: 
                    names      = self.__browser.find_elements_by_css_selector (names_selector)
                    prices     = self.__browser.find_elements_by_css_selector (prices_selector)
                    cuantities = self.__browser.find_elements_by_css_selector (cuantities_selector)
                    costs       = self.__browser.find_elements_by_css_selector (costs_selector)
                    time.sleep (1)
                
                
                # Save info in csv file
                self.__saveData (names, prices, cuantities, costs, order, outputWriter)
            outputFile.close()
        else: 
            print ('No new orders yet')
        




            



my_extractor = WebExtract ("kyitzchok", "freightNY")
my_extractor.login()