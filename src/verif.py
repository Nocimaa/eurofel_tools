#%%
from selenium.webdriver.chrome.service import Service as ChromeService
import os
if os.name=='nt':from subprocess import CREATE_NO_WINDOW
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
            if '404: Not Found' in self.browser.page_source:
                raise ValueError
            self.valid = True
        except:
            self.valid = False

# %%
