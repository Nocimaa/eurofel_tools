#%%
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import os
if os.name == 'nt': from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import abstract



class Facturation(abstract.Abstract):
    def __init__(self, excel,entrepot, zonegeo):
        super().__init__()
        self.main_excel=excel
        self.service=ChromeService()
        if os.name == 'nt':self.service.creation_flags= CREATE_NO_WINDOW
        options = Options()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.geo = zonegeo
        self.browser= webdriver.Chrome(service=self.service,options=options)  
        self.browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")
        self.excel = self.main_excel[self.main_excel['ENTREPOT']==entrepot]
        self.excel = self.excel.sort_values(by=['IFLS'])
        self.action=ActionChains(self.browser)

        self.entrepot=entrepot
        self.secteur="12" if entrepot == "175" else "2"
        self.date=self.excel.iloc[0]['JOUR']
        self.canal=self.excel.iloc[0]['CANAL']

        self.pas=excel['QUANTITE'].sum()
        self.ps=0

        self.etb={"175":"901","729":"961","774":"961"}
    
    def setup(self):
        self.full_process(self.entrepot)
        self.waiting_system()

        check = self.quantity_check()
        if not check:
            self.stopped = True
        if self.entrepot == '175':
            #self.generate_tarif()
            if self.canal == "R":
                self.generate_majser()
            #self.generate_tax()
            self.write(Keys.F3)
            self.waiting_system()
            self.write(Keys.F3)
            self.waiting_system()
        
        self.send_quantity()
        self.write(Keys.F3)
        self.waiting_system()
        self.write(Keys.F3)
        self.waiting_system()

        self.action.key_down(Keys.SHIFT).send_keys(Keys.F12).key_up(Keys.SHIFT).perform()
        self.waiting_system()
        self.write(Keys.F3)
        self.waiting_system()
        self.action.key_down(Keys.SHIFT).send_keys(Keys.F12).key_up(Keys.SHIFT).perform()
        self.waiting_system()
        self.write(Keys.F3)
        self.waiting_system()
        self.write(Keys.F3)
        self.waiting_system()


        self.facturation()



    def facturation(self):
        self.write(self.credentials.facturationpass)
        self.enter()
        time.sleep(3)
        if self.geo == "Rungis":
            self.tab(2)
        else:
            self.tab(1)
        self.write("1")
        self.enter()
        time.sleep(3)
        self.enter()

        self.write("11")
        self.waiting_system()
        
        liste = self.browser.execute_script("return document.getElementsByClassName('NGREEN');")
        self.tab(4)
        i = 0
        while liste[20 + i * 11].text.strip().isdigit():
            print(liste[20 + i * 11].text.strip().isdigit())
            i += 1

    def full_process(self,entrepot):
        self.loggin()
        self.choose_bassin(self.etb[entrepot])
        self.choose_entrepot(entrepot)

    def generate_tax(self):
        self.write("10")
        self.waiting_system()

        self.write(Keys.F6)
        self.waiting_system()

        if self.canal == "R":
            fl = "01500O00000"
            rs = "O"
            self.write("02")
        else:
            fl = "01000O00400"
            rs = "N" 
            self.write("01")
        self.write(fl)
        self.tab(4)
        self.write(rs)
        
        self.enter()
        self.enter()

        time.sleep(5)
        self.enter()
        self.enter()
        self.write(Keys.F3)

    def send_quantity(self):
        self.write("02")
        self.waiting_system()
        self.write("04")
        self.waiting_system()

        self.tab(1)
        self.write(self.date)
        self.tab(1)
        self.write(self.secteur)
        self.enter()
        self.waiting_system()


        while True:
            liste = self.browser.execute_script("return document.getElementsByClassName('NGREEN');")
            self.tab(3)
            for i in range(13):
                current = liste[24 + i * 10].text.strip()
                if not current.isdigit():
                    break
                self.write("Z")
            liste = self.browser.execute_script("return document.getElementsByClassName('NWHITE');")
            if 'Fin' in liste[-2].text.strip():
                self.enter()
                liste = self.browser.execute_script("return document.getElementsByClassName('NWHITE');")
                while liste[2].text == 'Saisie des commandes client':
                    self.write(Keys.F3)
                    self.waiting_system()
                    liste = self.browser.execute_script("return document.getElementsByClassName('NWHITE');")
                self.write(Keys.F3)

                break
            else:    
                self.write(Keys.PAGE_DOWN)
                self.waiting_system()
    def generate_majser(self):
        self.write("09")
        self.waiting_system()

        self.write(self.date)
        self.write("MAJSER")
        self.tab(1)
        self.write("999")
        self.tab(1)
        self.write("ONN")
        self.enter()
        self.enter()

        self.tab(10)
        self.suppr(10)
        self.write("60,00")
        self.enter()
        time.sleep(1.5)
        self.write(Keys.F3)
        self.waiting_system()
        self.write(Keys.F3)
        self.waiting_system()

    def generate_tarif(self):
        self.write("01")
        self.waiting_system()
        self.write("01")
        self.waiting_system()
        self.write("08")
        self.waiting_system()

        self.write(self.secteur)
        self.write(self.date)
        self.tab(3)
        self.write('N')
        self.enter()
        self.waiting_system()
        self.tab(1)
        self.write('O')
        self.waiting_system()
        self.enter()
        self.waiting_system()
        time.sleep(7)
        self.enter()
        self.waiting_system()
        self.enter()
        self.waiting_system()

    def quantity_check(self):
        self.write("02")
        self.waiting_system()
        self.write("04")
        self.waiting_system()

        self.tab(1)
        self.write(self.date)
        self.tab(1)
        self.write(self.secteur)
        self.enter()
        self.waiting_system()
        while True:
            liste = self.browser.execute_script("return document.getElementsByClassName('NGREEN');")
            for i in range(13):
                current = liste[24 + i * 10].text.strip()
                if not current.isdigit():
                    break
                self.ps += int(current)
            liste = self.browser.execute_script("return document.getElementsByClassName('NWHITE');")
            if 'Fin' in liste[-2].text.strip():
                break
            self.write(Keys.PAGE_DOWN)
            self.waiting_system()
        self.write(Keys.F3)
        self.waiting_system()
        self.write(Keys.F3)
        self.waiting_system()
        return self.pas <= self.ps
            
# %%
