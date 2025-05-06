from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_links(profession):
    options = ChromeOptions()
    win=Chrome(options=options)
    win.get('https://www.naukri.com/mnjuser/homepage')
    time.sleep(3)
    win.find_element(By.ID,'usernameField').send_keys('saubansamith021@gmail.com')
    win.find_element(By.ID,'passwordField').send_keys('Sauban@1234')
    win.find_element(By.CLASS_NAME,'blue-btn').click()
    time.sleep(5)
    win.find_element(By.CLASS_NAME,'nI-gNb-sb__main').click()
    win.find_element(By.CLASS_NAME,'dropdownMainContainer').click()
    win.find_element(By.XPATH,'//*[@id="sa-dd-scrolljobType"]/div[1]/ul/li[2]').click()
    win.find_element(By.CLASS_NAME,'suggestor-input').send_keys(profession)
    win.find_element(By.CLASS_NAME,'nI-gNb-sb__icon-wrapper').click()
    time.sleep(3)
    links=[]
    for link in win.find_elements(By.CLASS_NAME,'title '):
        links.append(link.get_attribute('href'))
    win.close()
    return links