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
        
        self.base_url = 'https://www.linkedin.com'
        self.login_url = self.base_url + '/login'
        self.feed_url = self.base_url + '/feed'
        self.analytics_follower_url = self.base_url + '/company/11030983/admin/analytics/followers/'
        
        self.username = username
        self.password = password
        
    def _nav(self, url):
        self.driver.get(url)
        time.sleep(3)
        
    def login(self, username, password):
        """Login to Linkedin account"""
        self._nav(self.login_url)
        self.driver.find_element_by_id('username').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_xpath("//button[contains(text(), 'identifier')]").click()
        
    def go_follower_page(self):
        self._nav(self.analytics_follower_url)
        
    def get_followers(self):
        self.driver.find_element_by_xpath("//button[@class='org-view-page-followers-module__modal-button t-16 p1 t-bold full-width'][@type='button'][@data-control-name='see_all_followers']").click()
        #scroll down to the bottom
        time.sleep(1)
        data=[]
        #self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        if self.driver.find_element_by_tag_name('table'):
            if self.driver.find_element_by_tag_name('tbody'):
                #element_inside_popup.send_keys(Keys.END)
                #for j in range(1, 413):
                for i in range(1, 412):
                    if (i <= 300 & i%20 == 0):
                        element_inside_popup = self.driver.find_element_by_xpath("/html/body/div[@id='artdeco-modal-outlet']/div[1]/div[1]/div[@class='artdeco-modal__content org-view-page-followers-modal__content artdeco-modal__content--no-padding ember-view']")
                        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', element_inside_popup)
                        time.sleep(3)
                        self.driver.execute_script('arguments[0].scrollBottom = arguments[0].scrollHeight', element_inside_popup)
                        time.sleep(3)
                    elif (i > 300 & i%10 == 0):
                        element_inside_popup = self.driver.find_element_by_xpath("/html/body/div[@id='artdeco-modal-outlet']/div[1]/div[1]/div[@class='artdeco-modal__content org-view-page-followers-modal__content artdeco-modal__content--no-padding ember-view']")
                        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', element_inside_popup)
                        time.sleep(10)
                    else:
                        pass
                    print("i={}".format(i))
                    try:
                        elem = self.driver.find_element_by_xpath("//table[@class='table']/tbody/tr[{}]/td[1]/a".format(i))
                        link = elem.get_attribute('href')
                    except:
                        link=''
                    try:
                        follower=self.driver.find_element_by_xpath("//table[@class='table']/tbody/tr[{}]/td[1]/a/div/div[2]/div[1]".format(i)).text
                    except:
                        follower=''
                    try:
                        degree=self.driver.find_element_by_xpath("//table[@class='table']/tbody/tr[{}]/td[1]/a/div/div[2]/div[2]/span[1]".format(i)).text
                    except:
                        degree=''
                    try:
                        headline=self.driver.find_element_by_xpath("//table[@class='table']/tbody/tr[{}]/td[1]/a/div/div[2]/div[3]/span[1]".format(i)).text
                    except:
                        headline=''
                    try:
                        follower_time=self.driver.find_element_by_xpath("//table[@class='table']/tbody/tr[{}]/td[2]/span[1]/span[1]".format(i)).text
                    except:
                        follower_time=''
                    person=[follower,degree,headline,follower_time,link]
                    print(follower+", followed at "+follower_time+", having "+degree+", with lien "+link+", is "+headline+" !")
                    data.append(person)
                else:
                    print("No more followers ! End !")
                # Create the pandas DataFrame 
                df = pd.DataFrame(data, columns = ['Name', 'ConnectionDegree', 'Headline', 'FollowedTime', 'link'])
                print("lentgh of df is ")
                print(len(df))
                df.info()
                df.to_csv('/Users/xiaoxiaosu/Documents/Codes/GitHub/Python/linkedin/OppchainLinkedinFollowers.csv') 
        
    def go_analytics(self):
        """go to page analytics"""
        self.driver.find_element_by_link_text('See visitor analytics').click()
        
    def download_visitor(self):
        """download followers statistics"""
        self.driver.find_element_by_tag_name('h4').click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@class='fr mlA mt3 artdeco-button artdeco-button--primary'][@type='button']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@class='fr ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']").click()
        

if __name__ == '__main__':
    
    username = linkedin_credentials.username
    password = linkedin_credentials.password
    
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "/Users/xiaoxiaosu/Documents/Codes/GitHub/Python/linkedin"}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "/Users/xiaoxiaosu/Downloads/chromedriver"
    
    bot = LinkedinBot(username, password, chromedriver, chromeOptions)
    bot.login(username, password)
    bot.go_analytics()
    #bot.download_visitor()
    bot.go_follower_page()
    time.sleep(1)
    bot.get_followers()
    