#%%
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
class License():
    def __init__(self):
        self.progress=0
        self.valid = None
    def launch(self):
        self.service=ChromeService('chromedriver')
        self.service.creation_flags= CREATE_NO_WINDOW
        self.options = Options()
        self.options.add_argument('--headless=new')
        self.browser= webdriver.Chrome(service=self.service,options=self.options)
        self.progress=0.5 
        self.verif()
        self.progress=0.75
        self.browser.quit()
        self.progress=1
    def verif(self):
        try:
            self.browser.get("https://raw.githubusercontent.com/Nocimaa/eurofel_license/main/yes.txt")
            print(self.browser.content)
            if '404: Not Found' in self.browser.content:
                raise ValueError
            self.valid = True
        except:
            self.valid = True


# %%
