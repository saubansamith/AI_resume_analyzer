from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_links(profession):
    # options = ChromeOptions()
    # # options.add_argument("--headless")  # Run Chrome in headless mode
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1920,1080")
    # # Add user-agent to avoid detection
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
    
    win=Chrome()
    win.get('https://www.naukri.com/mnjuser/homepage')
    time.sleep(3)
    win.find_element(By.ID,'usernameField').send_keys('saubansamith021@gmail.com')
    win.find_element(By.ID,'passwordField').send_keys('Sauban#1234')
    win.find_element(By.CLASS_NAME,'blue-btn').click()
    time.sleep(5)
    win.find_element(By.CLASS_NAME,'nI-gNb-sb__main').click()
    win.find_element(By.CLASS_NAME,'dropdownMainContainer').click()
    win.find_element(By.CLASS_NAME,'nI-gNb-sb__keywords').click()
    win.find_element(By.CLASS_NAME,'suggestor-input').send_keys(profession)
    win.find_element(By.CLASS_NAME,'nI-gNb-sb__icon-wrapper').click()
    time.sleep(3)
    jobs=[]
    for link in win.find_elements(By.CLASS_NAME,'title '):
        jobs.append((link.get_attribute('title'),link.get_attribute('href')))
    if None in jobs or len(jobs)==0:
            for link in win.find_elements(By.CLASS_NAME,'title '):
                jobs.append((link.get_attribute('title'),link.get_attribute('href')))

    win.close()
    return jobs



