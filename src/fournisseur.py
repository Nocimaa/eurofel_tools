#%%
import threading
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Fournisseur():
    def __init__(self,excel,entrepot):
        
        self.main_excel=excel
        self.service=ChromeService('chromedriver')
        self.service.creation_flags= CREATE_NO_WINDOW
        options = Options()
        #options.add_argument('--headless=new')
        self.browser= webdriver.Chrome(service=self.service,options=options)  
        self.browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")
        self.excel = self.main_excel[self.main_excel['ENTREPOT']==entrepot]
        self.action=ActionChains(self.browser)
        self.credentials= ["FRUBY5G","Mathieu2"]
        self.ffi = "F"

        self.start=False
        self.state=False

        self.entrepot=entrepot
        self.secteur="12" if entrepot == "175" else "2"
        self.date=self.excel.iloc[0]['DATE']
        self.fournisseurs_set=set(self.excel['FOURNISSEUR'])

        self.pas=len(self.excel)
        self.ps=0

        self.etb={"175":"901","729":"961","774":"961"}
        """
        self.ifls = self.excel['IFLS']
        self.entrepots = self.excel['ENTREPOT']
        self.code = self.excel['CODE FOURNISSEUR']
        self.prix =  self.excel['PRIX']
        self.quantite = self.excel['QUANTITE']
        self.fournisseurs=self.excel['FOURNISSEUR']
        """

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

    def get_first_item(self):
        while True:
            try:
                time.sleep(0.25)
                for i in range(4):
                    try:
                        h = self.browser.execute_script("return document.getElementsByClassName('NGREEN');")[25+i]
                        int(h.text)
                        return h.text
                    except:
                        if i==3:return None
            except:
                print("get_first crash")
                time.sleep(1)
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
    def qp_input(self,q,p):
        self.tab(5)
        self.suppr(7)
        self.write(q)
        self.tab(2)
        self.suppr(10)
        self.write(p)
        self.enter()
        self.waiting_system()
    
    def import_ifls(self,ifls):
        #f1_system()
        self.action.key_down(Keys.SHIFT).send_keys(Keys.F1).key_up(Keys.SHIFT)
        self.action.perform()
        self.waiting_system()
        self.action.send_keys(Keys.F6)
        self.action.perform()
        self.waiting_system()
        self.action.send_keys(Keys.TAB)
        self.action.perform()
        self.waiting_system()
        self.action.send_keys(Keys.F4)
        self.action.perform()
        self.waiting_system()
        self.tab(2)
        self.write(ifls)
        self.enter()
        self.waiting_system()
        if self.get_first_imported()!=ifls:
            for i in range(2):
                self.action.send_keys(Keys.F3)
                self.action.perform()
            return True
        self.tab(9)
        self.write("1")
        self.enter()
        self.waiting_system()
        self.enter()
        self.waiting_system()
        self.action.send_keys(Keys.F3)
        self.action.perform()
        if ifls!=self.get_first_item():
            return True
        else:
            return False
    def ifls_input(self,ifls):
        #f1_system()
        self.suppr(6)
        self.write(ifls)
        self.enter()
        self.waiting_system()

    def f(self,s):
        if len(s)== 5:s='0'+s
        return s
    def fourniformat(self,s):
        if len(s)<5:s="0"*(5-len(s))+s
        return s
    
    def starte(self,df):
        i=0
        #f1_system()
        while i<len(df):
            cur=df.iloc[i]
            #print(f"{i}: {self.entrepot} {cur['IFLS']} {cur['FOURNISSEUR']}")
            #f1_system()
            self.waiting_system()
            self.suppr(6)
            if int(cur['QUANTITE'])==0:
                i+=1
                self.ps+=1
                #self.main_excel[self.main_excel['IFLS']==cur['IFLS'] and self.main_excel['ENTREPOT'] == self.entrepot] = 'Ko: Quantity 0'
                continue    
            self.ifls_input(cur['IFLS'])
            if cur['IFLS']==self.get_first_item():
                pass
            else:
                if self.import_ifls(cur['IFLS']):
                    print(f"Cannot import: {self.entrepot} {cur['IFLS']}, {cur['FOURNISSEUR']}")
                    #self.excel[self.excel['IFLS']==cur['IFLS']]='Ko'
                    #self.main_excel[self.main_excel['IFLS']==cur['IFLS'] and self.main_excel['ENTREPOT'] == self.entrepot] = 'Ko: Product cannot be imported'
                    i+= 1
                    continue
            self.qp_input(str(cur['QUANTITE']),str(cur['PRIX']))
            i+=1
            #self.excel[self.excel['IFLS']==cur['IFLS']]['Status']='Ok'
            #self.main_excel[self.main_excel['IFLS']==cur['IFLS'] and self.main_excel['ENTREPOT'] == self.entrepot] = 'Ok'
            self.ps+=1
    def init(self,code):
        #f1_system()
        self.action.send_keys(Keys.F6)
        self.action.perform()
        self.waiting_system()
        if self.ffi=="Ferme":
            self.tab(1)
        if self.ffi=="Fictive":
            self.suppr(2)
            self.write("FI")
        self.write(code)
        if len(code)<=5:self.tab(1)
        self.suppr(8)
        self.write(self.date.replace("/",""))
        self.tab(2)
        self.write(self.secteur)
        self.enter()
        self.waiting_system()
        self.enter()
        self.waiting_system()
        self.action.send_keys(Keys.F6)
        self.action.perform()
        self.waiting_system()

    def setup(self):
        print("setup")
        self.full_process(self.entrepot)
        print(self.fournisseurs_set)
        for f in self.fournisseurs_set:
            curr = self.excel[self.excel['FOURNISSEUR']==f]
            time.sleep(1)
            self.init(curr['CODE FOURNISSEUR'].iloc[0])
            self.waiting_system()
            self.starte(curr)
            self.write(Keys.F3)
            self.waiting_system()
            self.write(Keys.F3)
            self.waiting_system()
        self.browser.close()
    def full_process(self,entrepot):
        self.loggin()
        self.choose_bassin(self.etb[entrepot])
        self.choose_entrepot(entrepot)
        self.action.send_keys("01")
        self.action.perform()
        self.waiting_system()
        self.action.send_keys("02")
        self.action.perform()
        self.waiting_system()
        self.action.send_keys("07")
        self.action.perform()
        self.waiting_system()
        
        
    def loggin(self):
        self.write(self.credentials[0])
        self.tab(1)
        self.write(self.credentials[1])
        self.enter()
        self.waiting_system()
        time.sleep(4)
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
