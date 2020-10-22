import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import linkedin_credentials

class LinkedinBot:
    def __init__(self, username, password, chromedriver, chromeOptions):
        """"""
        
        self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
        
        self.base_url = 'https://www.linkedin.com/uas/login?session_redirect=%2Fsales&fromSignIn=true&trk=navigator'
        self.test_url = 'https://www.linkedin.com/sales/search/people/list/saved-leads-for-account/3829?searchSessionId=BD1SHbOmQxSxbuol7eB8dA%3D%3D'
        
        self.lead_list_company_eti_url = 'https://www.linkedin.com/sales/lists/company/6723938983346360320?sortCriteria=CREATED_TIME'
        self.lead_list_company_eti_url_2 = 'https://www.linkedin.com/sales/lists/company/6723938983346360320?page=2&sortCriteria=CREATED_TIME'
        self.lead_list_company_eti_url_3 = 'https://www.linkedin.com/sales/lists/company/6723938983346360320?page=3&sortCriteria=CREATED_TIME'
        
        self.username = username
        self.password = password
        
    def _nav(self, url):
        self.driver.get(url)
        time.sleep(3)
        
    def login(self, username, password):
        """Login to Linkedin account"""
        self._nav(self.base_url)
        self.driver.find_element_by_id('username').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_xpath("//button[contains(text(), 'identifier')]").click()
        
    def get_test_info(self):
        self._nav(self.test_url)
        time.sleep(5)
        for a in range(1, 4):
        # each page there is 25 leads
            for i in range(1, 26):
                # *****************************************
                # 1. go to the corresponding page
                # *****************************************
                if (a == 1):
                    self.go_to_page_liste_company_eti_url()
                elif (a == 2):
                    self._nav(self.lead_list_company_eti_url_2)
                else:
                    self._nav(self.lead_list_company_eti_url_3)
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                # get company link
                try:
                    elem = self.driver.find_element_by_xpath("//table/tbody/tr[{}]/td[@class='artdeco-models-table-cell list-company-detail-header__entity ember-view']/div/dl/div/dt/a".format(i))
                    link = elem.get_attribute('href')
                except:
                    link=''
                print("link is "+link)
                if (link != ''):
                    # get number of prospects
                    try:
                        num_lead = self.driver.find_element_by_xpath("//table/tbody/tr[{}]/td[@class='artdeco-models-table-cell list-company-detail-header__save-leads ember-view']/div/a/span".format(i)).text
                    except:
                        num_lead = '0'
                    print("number of prospects is "+num_lead)
                    num = int(num_lead)
                    if (num == 0):
                        # go to prospect page by click
                        continue
                        # enter keyword for search
                        # click enter
                        # collect result
                    else:
                        pass
                else:
                    break
                    
        
        
if __name__ == '__main__':
    
    username = linkedin_credentials.username
    password = linkedin_credentials.password
    
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "/Users/xiaoxiaosu/Documents/Codes/GitHub/Python/linkedin"}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "/Users/xiaoxiaosu/Downloads/chromedriver"
    
    bot = LinkedinBot(username, password, chromedriver, chromeOptions)
    # login
    bot.login(username, password)
    time.sleep(1)
