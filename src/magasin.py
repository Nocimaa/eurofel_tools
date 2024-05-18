#%%
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import os
if os.name == 'nt': from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from pandas import read_excel
from selenium.webdriver.chrome.options import Options
#%%

#excel=read_excel('carrefour.magasin test.xlsx', sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':str,'FOURNISSEUR':str,'DATE':str,'JOUR':str,'CANAL':str,'MAGASIN':str})

#%%
class Magasin():
    def __init__(self,main_excel,entrepot,credentials):
        
        
        self.service=ChromeService()
        if os.name == 'nt':self.service.creation_flags= CREATE_NO_WINDOW
        options = Options()
        #options.add_argument('--headless=new')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.browser= webdriver.Chrome(service=self.service,options=options)
        self.browser.minimize_window()
        self.browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")
        self.main_excel = main_excel
        self.excel = main_excel[main_excel['ENTREPOT']==entrepot]
        self.excel = self.excel.sort_values(by=['MAGASIN','IFLS'])
        self.action=ActionChains(self.browser)
        self.credentials= credentials

        self.start=False
        self.state=False

        self.entrepot=entrepot
        self.secteur="12" if entrepot == "175" else "2"
        self.date=self.excel.iloc[0]['JOUR']
        self.ifls_set=list(set(self.excel['IFLS']))
        self.ifls_set.sort()

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
            if h.text.isalpha():return h.text
            int(h.text)
            if len(h.text)!=6:raise ValueError
            return h.text
        except:
            pass
        try:
            h = self.browser.execute_script("return document.getElementsByClassName('NPINK');")[1]
            if h.text.isalpha():return h.text
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
        if self.browser.execute_script("return document.getElementsByClassName('NWHITE');")[0].text.strip()=="Messages":
            self.enter()
            self.waiting_system()
    def setup(self):
        self.full_process(self.entrepot)
        self.waiting_system()
        for ifls in self.ifls_set:
            exc=self.excel[self.excel['IFLS']==ifls].sort_values(by=['MAGASIN'],ascending=False)
            if not self.create_fp(exc):continue
            self.waiting_system()
            self.input_market(exc)
            self.waiting_system()
        self.browser.close()
        self.main_excel.to_excel('Rapport Magasin.xlsx')
    def create_fp(self,exc):
        cur = exc.iloc[0]
        self.write(Keys.F6)
        self.waiting_system()
        self.write(Keys.F4)
        self.waiting_system()
        self.tab(2)
        self.write(cur['IFLS'])
        self.enter()
        if self.get_first_imported() != cur['IFLS']:
            self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==cur['IFLS']),'Status']='Ko: IFLS cannot be used'
            self.write(Keys.F3)
            self.waiting_system()
            self.write(Keys.F3)
            self.waiting_system()
            return False
        self.tab(9)
        self.write("1")
        self.enter()
        self.waiting_system()
        self.tab(2)
        self.write(cur['CANAL'])
        self.tab(1)
        self.suppr(8)
        self.write(cur['JOUR'])
        self.enter()
        self.waiting_system()
        if len(self.browser.execute_script("return document.getElementsByClassName('NWHITE');"))!= 5:
            self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==cur['IFLS']),'Status']='Ko: IFLS cannot be used'
            self.tab(1)
            self.write('N')
            self.write(Keys.F3)
            self.waiting_system()
            return False
        self.enter()
        self.waiting_system()
        if self.browser.execute_script("return document.getElementsByClassName('NWHITE');")[2].text =='Critères de sélection':
            self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==cur['IFLS']),'Status']='Ko: IFLS cannot be used'
            self.write('N')
            self.write(Keys.F3)
            self.waiting_system()
            return False
        return True    
    def input_market(self,exc):
        t=dict(zip(exc['MAGASIN'],exc['QUANTITE']))
        ifls = exc.iloc[0]['IFLS']
        while len(t.keys())!=0:
            h=self.browser.execute_script("return document.getElementsByClassName('NGREEN');")
            self.tab(1)
            try:
                if int(h[23+7*11].text.strip())<int(min(t)):
                    self.write(Keys.PAGE_DOWN)
                    self.waiting_system()
                    continue
            except: pass
            for i in range(12):
                try:
                    if h[23+7*i].text.strip() in t.keys():
                        self.write(t[h[23+7*i].text.strip()])
                        self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==ifls)&(self.main_excel['MAGASIN'] == t[h[23 + 7 * i].text.strip()]),'Status']='Ok'
                        t.pop(h[23+7*i].text.strip())
                        self.ps+=1
                    
                except: pass
                if len(t.keys())==0:break
                self.tab(1)
            try:    
                code=h[23+7*11].text.strip()
                dic={el for el in t.keys() if int(el) < int(code)}
                for el in dic:
                    self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==ifls)&(self.main_excel['MAGASIN'] == el),'Status']='Magasin introuvable'
                    t.pop(el)
            except: pass
            self.write(Keys.PAGE_DOWN)
            self.waiting_system()
        self.enter()
        self.waiting_system()
        self.write(Keys.F3)
        self.waiting_system()
        #self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==ifls),'Status']='Ok'
    def full_process(self,entrepot):
        self.loggin()
        self.choose_bassin(self.etb[entrepot])
        self.choose_entrepot(entrepot)
        self.action.send_keys("02")
        self.action.perform()
        self.waiting_system()
        self.action.send_keys("04")
        self.action.perform()
        self.waiting_system()       
    def loggin(self):
        self.write(self.credentials.username)
        self.tab(1)
        self.write(self.credentials.passwd)
        self.enter()
        self.waiting_system()
        time.sleep(5)
        while self.verif()==0:
            self.enter()
            self.waiting_system()
        self.write(self.credentials.secndpasswd)
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
        self.write(self.etb[entrepot])
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
