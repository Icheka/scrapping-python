import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import linkedin_credentials
from datetime import datetime


now=datetime.now()
time_insert=now.strftime("%Y%m%d%H%M%S")

class LinkedinBot:
    def __init__(self, username, password, chromedriver, chromeOptions):
        """"""
        
        self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
        
        self.base_url = 'https://www.linkedin.com/uas/login?session_redirect=%2Fsales&fromSignIn=true&trk=navigator'    #'https://www.linkedin.com'
        self.login_url = self.base_url + '/login'
        self.feed_url = self.base_url + '/feed'
        self.analytics_follower_url = self.base_url + '/company/11030983/admin/analytics/followers/'
        self.lead_list_people_url = 'https://www.linkedin.com/sales/lists/people'
        self.lead_list_company_url = 'https://www.linkedin.com/sales/lists/company'
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
    
    def go_to_page_liste_people(self):
        self._nav(self.lead_list_people_url)
        
    def go_to_page_liste_company(self):
        self._nav(self.lead_list_company_url)
        
    def go_to_page_liste_company_eti_url(self):
        self._nav(self.lead_list_company_eti_url)
    
    def go_to_list_company_eti(self):
        self.driver.find_element_by_xpath("//div[@class='list-hub__name--max-width text-overflow-ellipsis overflow-hidden white-space-nowrap']").click()
        
    def get_lead_company(self):
        data=[]
        # 3 pages in total
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
                # ******************************************
                # 2. get data from diff pages
                # ******************************************
                #
                # ------------------------------------------
                # step 1: get companies
                # ------------------------------------------
                # (1)company link
                try:
                    elem = self.driver.find_element_by_xpath("//table/tbody/tr[{}]/td[@class='artdeco-models-table-cell list-company-detail-header__entity ember-view']/div/dl/div/dt/a".format(i))
                    link = elem.get_attribute('href')
                except:
                    link=''
                print("link is "+link)
                # (2)company name
                try:
                    company=self.driver.find_element_by_xpath("//table/tbody/tr[{}]/td[@class='artdeco-models-table-cell list-company-detail-header__entity ember-view']/div/dl/div/dt/a".format(i)).text
                except:
                    company=''
                print("company is "+company)
                # (3) company location
                try:
                    location=self.driver.find_element_by_xpath("//table/tbody/tr[{}]/td[@class='artdeco-models-table-cell list-company-detail-header__entity ember-view']/div/dl/dd[@class='list-company-detail__geography']".format(i)).text
                except:
                    location=''
                print("location is "+location)
                # (4)company category
                try:
                    category=self.driver.find_element_by_xpath("//table/tbody/tr[{}]/td[@class='artdeco-models-table-cell list-company-detail-header__entity ember-view']/div/dl/dd[@class='list-company-detail__industry']".format(i)).text
                except:
                    category=''
                print("category is "+category)
                # (5)number of employee
                try:
                    num_emp=self.driver.find_element_by_xpath("//table/tbody/tr[{}]/td[@class='artdeco-models-table-cell list-company-detail-header__entity ember-view']/div/dl/dd[@class='list-company-detail__employee-count']".format(i)).text
                except:
                    num_emp=''
                print("employee is "+num_emp)
                # (6)number of prospects
                try:
                    num_lead = self.driver.find_element_by_xpath("//table/tbody/tr[{}]/td[@class='artdeco-models-table-cell list-company-detail-header__save-leads ember-view']/div/a/span".format(i)).text
                except:
                    num_lead = '0'
                print("number of prospects is "+num_lead)
                # (7)prospect link
                try:
                    lead_elem = self.driver.find_element_by_xpath("//table/tbody/tr[{}]/td[@class='artdeco-models-table-cell list-company-detail-header__save-leads ember-view']/div/a".format(i))
                    lead_link = lead_elem.get_attribute('href')
                except:
                    lead_link=''
                print("prospect link is "+lead_link)
                # ---------------------------------------------------------------
                # step 2-1: go to company page and get site-web/siege
                # ---------------------------------------------------------------
                if (link != ''):
                    self._nav(link)
                    time.sleep(3)
                    # company site web
                    try:
                        elem_site=self.driver.find_element_by_xpath("//main/div[@class='header-wrapper']/div[@class='top-card']/div[@class='entity-card company banner']/div[@class='right actions-container mt1']/div[@class='meta-links']/div[1]/span/a".format(i))
                        site_web = elem_site.get_attribute('href')
                    except:
                        site_web=''
                    print("site_web is "+site_web)
                    # company siege
                    try:
                        elem_siege=self.driver.find_element_by_xpath("//main/div[@class='header-wrapper']/div[@class='top-card']/div[@class='entity-card company banner']/div[@class='right actions-container mt1']/div[@class='meta-links']/div[2]/span/a".format(i))
                        siege = elem_siege.get_attribute('href')
                    except:
                        siege=''
                    print("siege is "+siege)
                    # ----------------------------------------------------
                    # step 2-2: go to prospect url and get prospects
                    # ----------------------------------------------------
                    num = int(num_lead)
                    if (num != 0):
                        self._nav(lead_link)
                        time.sleep(10)
                        # Scroll down to bottom
                        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(5)
                        # get prospects
                        for j in range(1, num+1):
                            # scroll un element
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*{}/13);".format(j))
                            # 1) name
                            try:
                                prospect_name = self.driver.find_element_by_xpath("//ol[@class='search-results__result-list']/li[{}]/div[2]/div/div/div/article/section[@class='result-lockup']/div/div/dl/dt/a".format(j)).text
                            except:
                                try:
                                    time.sleep(10)
                                    prospect_name = self.driver.find_element_by_xpath("//ol[@class='search-results__result-list']/li[{}]/div[2]/div/div/div/article/section[@class='result-lockup']/div/div/dl/dt/a".format(j)).text
                                except:
                                    prospect_name=''
                            print("prospect name is "+prospect_name)
                            time.sleep(1)
                            # 2) poste
                            try:
                                prospect_poste = self.driver.find_element_by_xpath("//ol[@class='search-results__result-list']/li[{}]/div[2]/div/div/div/article/section[@class='result-lockup']/div/div/dl/dd[@class='result-lockup__highlight-keyword']/span[@class='t-14 t-bold']".format(j)).text
                            except:
                                prospect_poste=''
                            print("prospect poste is "+prospect_poste)
                            time.sleep(1)
                            # add to list: data
                            prospect=[company,link,location,category,num_emp,num_lead,prospect_name,prospect_poste,site_web,siege]
                            print(prospect)
                            data.append(prospect)
                            print("\n")
                    else:
                        prospect_name='NA'
                        prospect_poste='NA'
                        print("prospect name is "+prospect_name)
                        print("prospect poste is "+prospect_poste)
                        prospect=[company,link,location,category,num_emp,num_lead,prospect_name,prospect_poste,site_web,siege]
                        print(prospect)
                        data.append(prospect)
                        print("\n")
                else:
                    print("######################################")
                    print("No more comanies and prospects ! End !")
                    print("######################################")
                    break
            else:
                print("*****************************")
                print("Page {} end !".format(a))
                print("*****************************")
                print("\n\n\n")
        # *********************************************
        # 3. save data to pandas DataFrame and into CSV
        # *********************************************
        df = pd.DataFrame(data, columns = ['company', 'link', 'location', 'category', 'num_emp', 'num_lead', 'prospect_name', 'prospect_poste', 'site_web', 'siege'])
        print("lentgh of df is ")
        print(len(df))
        df.info()
        df.to_csv('/Users/xiaoxiaosu/Documents/Codes/GitHub/Python/linkedin/Scrapping/OppchainLinkedinProspect_ETI_CA_100-400M_ALL_{}.csv'.format(now_format)) 
        
        
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
    # go to lead company page
    bot.go_to_page_liste_company()
    time.sleep(2)
    # get lead company one by one
    bot.get_lead_company()
    time.sleep(1)
