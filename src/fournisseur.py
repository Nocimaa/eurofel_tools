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
import re

import json
with open("country.json", "r", encoding="utf-8") as file:
    dic = json.loads(file.read())
import re
re_vrac = r" Vrac (\d+,?\d*) k?g | Plateau (\d+,?\d*) k?g | \d+ rang (\d+,?\d*) k?g | Palox (\d+,?\d*) k?g | Mini colis (\d+,?\d*) k?g | Sac (\d+,?\d*) k?g | Mini colis plateau - (\d+,?\d*) k?g "
match_vrac = re.compile(re_vrac)
re_pcb = r" Barquettes (\d+)x\d* k?g | Vrac (\d+,?\d*) pcs - \d+,?\d* k?g | - (\d*,?\d*) pcs - \d*,?\d* k?g | Plateau (\d+) pcs - \d+,?\d* k?g | Bottes (\d*)x\d* k?g | Filets (\d+,?\d*)x\d+,?\d* k?g | Sachet (\d+,?\d*)x\d+,?\d* k?g | Girsac (\d+,?\d*)x\d+,?\d* k?g | Mini colis (\d+,?\d*)x\d+,?\d* k?g "
match_pcb = re.compile(re_pcb)


class Fournisseur(abstract.Abstract):
    def __init__(self,excel,entrepot, zonegeo):
        
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
        self.ffi = "Ferme"

        self.start=False

        self.state=False

        self.entrepot=entrepot
        self.secteur="12" if entrepot == "175" else "2"
        self.date = self.excel.iloc[0]['DATE']
        self.fournisseurs_set = set(self.excel['FOURNISSEUR'])

        self.pas = len(self.excel)
        self.ps = 0
        self.sw = 0
        self.hw = 0


        self.etb={"175":"901","729":"961","774":"961"}


    def get_first_item(self):
        while True:
            try:
                time.sleep(0.25)
                for i in range(4):
                    try:
                        h = self.browser.execute_script("return document.getElementsByClassName('NGREEN');")[25+i]
                        if h.text == "MAJSER":
                            return h.text 
                        int(h.text)
                        return h.text
                    except:
                        if i==3:return None
            except:
                print("get_first crash")
                time.sleep(1)

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
        while i<len(df):
            cur=df.iloc[i]
            self.waiting_system()
            self.suppr(6)
            if int(cur['QUANTITE'])==0:
                i+=1
                self.ps+=1
                self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==cur['IFLS']),'Status']='Quantité 0'
                continue  
            if float(cur['PRIX'].replace(',','.'))==0:
                i+=1
                #Ecrire Ko
                self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==cur['IFLS']),'Status']='Ko: Prix Zéro'
                continue  
            self.ifls_input(cur['IFLS'])
            if cur['IFLS']==self.get_first_item():
                pass
            else:
                if self.import_ifls(cur['IFLS']):
                    print(f"Cannot import: {self.entrepot} {cur['IFLS']}, {cur['FOURNISSEUR']}")
                    self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==cur['IFLS']),'Status']='Ko: Cannot Be imported'
                    i+= 1
                    continue

            warning = self.check_warning(cur)

            self.qp_input(str(cur['QUANTITE']),str(cur['PRIX']))
            i+=1
            self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==cur['IFLS']),'Status']='Ok'
            self.main_excel.loc[(self.main_excel['ENTREPOT']==self.entrepot)&(self.main_excel['IFLS']==cur['IFLS']),'Warning']=warning
            self.ps+=1
    def extract_tuple(self, tuple):
        return list(filter(lambda x : x != None, tuple))[0]
    def check_warning(self, df):
            if df['PRODUIT'] == "FRAIS LOGISTIQUE":
                return
            warning = ""
            liste = df['PRODUIT'].split('/')
            origine = str.lower(liste[-1].strip())

            listeWE = self.browser.execute_script("return document.getElementsByClassName('NGREEN');")
            i = 32 if listeWE[32].text.strip() in dic.keys() or len(listeWE[32].text.strip()) == 0 else 31
            pcb = int(listeWE[i + 1].text.strip())
            eurofel_origine = listeWE[i].text.strip()
            listeWE = self.browser.execute_script("return document.getElementsByClassName('NWHITE');")
            poids = float(listeWE[13].text.strip().replace(",", "."))
            
            if len(eurofel_origine) == 0:
                warning += f"Pas d'origine: Excel {origine} "
                self.sw += 1
            elif origine != str.lower(dic[eurofel_origine]):
                warning += f"Origine: Eurofel {dic[eurofel_origine]} Excel {origine} "
                self.sw += 1

            for el in liste[1:-1]:
                matched = match_pcb.match(el)
                if matched != None:
                    value = int(self.extract_tuple(matched.groups()))
                    if value != pcb:
                        warning += f"PCB: Eurofel {pcb} Excel {value} "
                        self.hw += 1
                    break

                matched = match_vrac.match(el)
                if matched != None:
                    value = float(self.extract_tuple(matched.groups()).strip().replace(",","."))
                    if value != poids:
                        warning += f"Poids: Eurofel {poids} Excel {value} "
                        self.hw += 1
                    break

            else:
                warning += f"Le libélé ne match contacte Antoine il comprendra, c'est pas grave verifie juste a la main et ca sera corriger plus tards tkt pas ca va bien se passer"
                self.sw += 1
            return warning

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
        try:
            int(code)
        except:
            return False
        self.write(code)
        if len(code)<=5:self.tab(1)
        self.suppr(8)
        self.write(self.date.replace("/",""))
        self.tab(2)
        self.write(self.secteur)
        #Zone Geo
        self.tab(3)
        print(self.geo)
        if (self.geo != 'Rungis'):
            self.write(str.upper(self.geo))
        #Fin Zone Geo
        self.enter()
        self.waiting_system()
        self.enter()
        self.waiting_system()
        self.action.send_keys(Keys.F6)
        self.action.perform()
        self.waiting_system()
        return True

    def setup(self):
        self.full_process(self.entrepot)
        for f in self.fournisseurs_set:
            curr = self.excel[self.excel['FOURNISSEUR']==f]
            time.sleep(1)
            if not self.init(curr['CODE FOURNISSEUR'].iloc[0]):
                self.write(Keys.F3)
                continue
            self.waiting_system()
            self.starte(curr)
            self.write(Keys.F3)
            self.waiting_system()
            self.write(Keys.F3)
            self.waiting_system()
        self.browser.close()
        for i in range(100):
            try:
                self.main_excel.to_excel(f'Rapport Fournisseur_{i}.xlsx')
                break
            except:
                pass

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
        
# %%
