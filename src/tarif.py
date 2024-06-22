#%%
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import os
if os.name == 'nt': from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import math
import datetime
import abstract
#excel=read_excel('carrefour.magasin test.xlsx', sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':str,'FOURNISSEUR':str,'DATE':str,'JOUR':str,'CANAL':str,'MAGASIN':str})
#%%
class Tarif(abstract.Abstract):
    def __init__(self, excel, entrepot, canal):
        
        super().__init__()  
        self.service = ChromeService()
        self.service.creation_flags = CREATE_NO_WINDOW
        options = Options()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.browser= webdriver.Chrome(service=self.service,options=options)  
        self.browser.get("https://pace.fr.carrefour.com/eurofel_prdv2/webaccess/")
        self.main_excel = excel
        self.excel = self.main_excel[self.main_excel['ENTREPOT']==entrepot]
        self.excel = self.excel.sort_values(by=['IFLS'])
        self.action=ActionChains(self.browser)

        self.start=False
        self.state=False

        self.entrepot = entrepot
        self.secteur = "12" if entrepot == "175" else "2"
        self.date = self.excel.iloc[0]['DATE']
        self.fournisseurs_set = set(self.excel['FOURNISSEUR'])
        self.canal = canal
        self.pas=len(self.excel)
        self.ps=0

        self.etb={"175":"901","729":"961","774":"961"}
        if entrepot!='175':
            date = datetime.date(2000+int(self.date[4:]),int(self.date[2:4]),int(self.date[:2]))
            date = date+datetime.timedelta(1)
            if date.weekday()==6:            
                date = date+datetime.timedelta(1)
            self.date=date.strftime('%d%m%y')

    def get_tax(self, line):

        if (line.iloc[0]['IFLS'] == 'MAJSER'):
            return 60

        prix = float(line.iloc[0]['PRIX'].replace(",","."))

        if self.canal == "R":
            return math.floor(1.15 * prix * 100) / 100
        else:
            return math.floor(1.144 * prix * 100) / 100
    
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

    def verif_tarif(self):
        while True:
            try:
                if len(self.browser.execute_script("return document.getElementsByClassName('NWHITE');"))==5:
                    return False
                self.enter()
                self.waiting_system()
                if self.browser.execute_script("return document.getElementsByClassName('NWHITE');")[1].text=="MODIFICATION D'UN TARIF":
                    return True
                if self.browser.execute_script("return document.getElementsByClassName('NWHITE');")[1].text=="GENERATION DU TARIF POUR 1 ARTICLE":
                    return False
            except:pass
    def tarif(self,ifls):

        #if multiple times this line in the file avoid crash
        quantity = list(self.excel[self.excel['IFLS']==ifls]['QUANTITE'])[0]


        if quantity==0:
            print('Cannot create tarif')
            self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==ifls),'Status']='Ko: Quantity Zero'
            return
        self.write(self.date)
        self.write(Keys.F4)
        self.waiting_system()
        self.tab(2)
        self.write(ifls)
        self.enter()
        if self.get_first_imported()!= ifls:
            self.write(Keys.F3)
            self.tab(5)
            self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==ifls),'Status']='Ko: IFLS cannot be found.'
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
            self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==ifls),'Status']='Ko: Aucune commande trouvé concernant cet IFLS'
            return

        if self.entrepot == '175':
            line = self.get_tax(self.excel[self.excel['IFLS'] == ifls])
            prix = self.get_tax(line)

        self.enter()
        self.waiting_system()
        self.write(Keys.F3)
        self.ps+=1
        self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==ifls),'Status']='Ok'
        self.waiting_system()
    
    def setup(self):
        self.full_process(self.entrepot)
        ite = sorted(list(set(self.excel['IFLS'])))
        for ifls in ite:
            self.tarif(ifls)
        self.browser.close()
        self.main_excel.to_excel('Rapport Tarif.xlsx')
        
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
        
# %%
