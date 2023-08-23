#%%
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pandas import read_excel
#%%
class Tarif():
    def __init__(self,excel,entrepot):
        
        
        self.service=ChromeService('chromedriver')
        self.service.creation_flags= CREATE_NO_WINDOW
        options = Options()
        self.browser= webdriver.Chrome(service=self.service,options=options)  
        self.browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")
        self.excel = excel
        self.action=ActionChains(self.browser)
        self.credentials= ["FRUBY5G","Mathieu2"]

        self.start=False
        self.state=False

        self.entrepot=entrepot
        self.secteur="12" if entrepot == "175" else "2"
        self.date=self.excel.iloc[0]['DATE']
        self.fournisseurs_set=set(self.excel['FOURNISSEUR'])

        self.pas=len(self.excel)
        self.ps=0

        self.etb={"175":"901","729":"961","774":"961"}

    #Process
    def enter(self):
        self.action.send_keys(Keys.ENTER)
        self.action.perform()
    def tab(self,i):
        for _ in range(i):self.action.send_keys(Keys.TAB)
        self.action.perform()
    def suppr(self,i):
        for _ in range(i):self.action.send_keys(Keys.DELETE)
        self.action.perform()
    def write(self,text):
        self.action.send_keys(text)
        self.action.perform()

    def get_first_imported(self):
        self.waiting_system()
        try:
            h = self.browser.execute_script("return document.getElementsByClassName('NGREEN');")[24]
            int(h.text)
            if len(h.text)!=6:raise ValueError
            return h.text
        except:
            pass
        try:
            h = self.browser.execute_script("return document.getElementsByClassName('NPINK');")[1]
            int(h.text)
            if len(h.text)!=6:raise ValueError
            return h.text
        except:
            pass
        print('Cannot be imported')
        
        return None

    def waiting_system(self):
        time.sleep(0.1)
        while True:
            time.sleep(0.1)
            try:
                h = self.browser.execute_script("return document.getElementById('sb_status');")
                if not "X SYSTEM" in h.text:
                    time.sleep(0.1)
                    break
            except:
                time.sleep(0.25)
        if  self.browser.execute_script("return document.getElementsByClassName('NWHITE');")[0].text.strip()=="Messages":
            self.enter()
            self.waiting_system()
    def verif_tarif(self):
        while True:
            try:
                if len(self.browser.execute_script("return document.getElementsByClassName('NWHITE');"))==5:
                    return False
                self.enter()
                self.waiting_system()
                if self.browser.execute_script("return document.getElementsByClassName('NWHITE');")[1].text=="MODIFICATION D'UN TARIF":
                    return True
            except:pass
    def tarif(self,ifls):
        self.write(self.date)
        self.write(Keys.F4)
        self.waiting_system()
        self.tab(2)
        self.write(ifls)
        self.enter()
        if self.get_first_imported()!= ifls:
            self.write(Keys.F3)
            self.tab(5)
            print("Cannot create tarif for ", ifls)
            return
        self.tab(9)
        self.write('1')
        self.enter()
        self.waiting_system()
        self.tab(2)
        self.write('ONN')
        self.enter()
        self.waiting_system()
        self.enter()
        if not self.verif_tarif():
            print("Cannot create tarif for ", ifls)
            return                
        self.enter()
        self.waiting_system()
        self.write(Keys.F3)
        self.ps+=1
        self.waiting_system()
    
    def setup(self):
        self.full_process(self.entrepot)
        for ifls in set(self.excel['IFLS']):
            self.tarif(ifls)
        
    def full_process(self,entrepot):
        self.loggin()
        self.choose_bassin(self.etb[entrepot])
        self.choose_entrepot(entrepot)
        self.action.send_keys("01")
        self.action.perform()
        self.waiting_system()
        self.action.send_keys("01")
        self.action.perform()
        self.waiting_system()
        self.action.send_keys("09")
        self.action.perform()
        self.waiting_system()
        
        
    def loggin(self):
        self.write(self.credentials[0])
        self.tab(1)
        self.write(self.credentials[1])
        self.enter()
        self.waiting_system()
        time.sleep(5)
        while self.verif()==0:
            self.enter()
            self.waiting_system()
        self.write(self.credentials[0])
        self.enter()
        self.waiting_system()

    def choose_bassin(self,bassin):
        if bassin=="901":
            self.tab(1)
        if bassin=="961":
            self.tab(2)
        self.write("1")
        self.enter()
        self.waiting_system()
        while self.verif()==0:
            self.enter()
            self.waiting_system()

    def choose_entrepot(self,entrepot):
        self.write("07")
        self.write(entrepot)
        self.enter()
        self.waiting_system()
        self.tab(4)
        self.write("1")
        self.enter()
        self.waiting_system()
    
    def verif(self):
        h = self.browser.execute_script("return document.getElementsByClassName('RGREEN');")
        return len(h)
# %%
