# webdriver imports and os import for setting driver path variable
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# from selenium.webdriver.support.wait import WebDriverWait

# table extraction imports
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://magicpin.in/New-Delhi/Paharganj/Restaurant/Eatfit/store/61a193/delivery/'
class Extractor(webdriver.Chrome):

    def __init__(self, driver_path="G:/SeleniumDrivers" ,teardown=False):
        '''
        input-
            driver_path(PATH): specifies path to chromedriver.exe
            teardown(boolean): if true, browser will not close after opening the landing page
        function -
            initializes the driver and sets the driver path in os environment
            sets the teardown variable to prevent browser from closing immediately
        '''
        self.driver_path = driver_path
        self.teardown = teardown #prevents webpage from closing immediately
        os.environ['PATH'] += self.driver_path #sets driver path in os environments
        options = webdriver.ChromeOptions()
        super(Extractor,self).__init__(options=options)
        self.maximize_window()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        function- 
            prevents browser from closing
        '''
        if self.teardown:
            self.quit()
        else:
            while(True): #browser keeps on closing after opening, hence I thought of this idea, if i keep loop running, then it won't close the browser
                pass

    def landing_page(self):
        '''
        function -
            driver launches the landing page
        '''
        self.get(BASE_URL)
        time.sleep(3)

    def click_dropdowns(self):
        """
        Clicks on all dropdown headers in the web page to reveal hidden content.

        This function iterates through all dropdown headers identified by the class 'subListingsHeader'
        and simulates a click action on each header, causing the associated content to be displayed.

        Parameters:
            None

        Returns:
            None
        """
        dropdown_headers = self.find_elements(By.CLASS_NAME,'subListingsHeader')
        for dropdown in dropdown_headers:
            dropdown.click()
            time.sleep(1)
    
    def extract_soup_object(self):
        """
        Extracts a BeautifulSoup object from a specified div element and prints its text content.

        This function retrieves the outer HTML content of a specific div element identified by the class
        'catalogItemsHolder' using Selenium. It then creates a BeautifulSoup object and prints its text content.

        Parameters:
            None

        Returns:
            None
        """

        div_element = self.find_element(By.CLASS_NAME,'catalogItemsHolder').get_attribute("outerHTML")
        soup = BeautifulSoup(div_element, 'html.parser')
        print('soup initialized \n\n')

        food_items = soup.find_all('section', class_='categoryItemHolder')

        for item in food_items:
            food_name = item.find('p', class_='itemName').text.strip()
            food_price = item.find('span', class_='itemPrice').text.strip()
            print(f"Food: {food_name}\t\t, Price: {food_price}")

#for code modularity, below code can be a separate run.py file with imports of Extractor class 
with Extractor() as e:
    e.landing_page()
    e.click_dropdowns()
    e.extract_soup_object()
