import threading
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys




class Procedure():
    def __init__(self,browser,excel):
        self.browser = browser
        self.excel = excel
        self.action=ActionChains(browser)


        self.start=False
        self.state=False

        self.entrepot=None
        self.secteur=None
        self.date=None
        self.fournisseurs_set=set()

        self.pas=0
        self.ps=0


        self.ifls = self.excel['IFLS']
        self.entrepots = self.excel['ENTREPOT']
        self.code = self.excel['CODE FOURNISSEUR']
        self.prix =  self.excel['PRIX']
        self.quantite = self.excel['QUANTITE']
        self.fournisseurs=self.excel['FOURNISSEUR']

        self.L=[]

    def get_Entrepot(self):
        try:
            h=self.browser.execute_script("return document.getElementsByClassName('NWHITE')")[0]
            if h.text in ['175','729','774']:
                self.entrepot=h.text
                return True
            else:return False
        except:
            return False
    
    def get_secteur(self):
        if self.entrepot == '175':self.secteur='12'
        else:self.secteur='2'
        return True
    def get_date(self):
        try:
            self.date=self.excel['DATE'][0]
            return True
        except:return False
    
    def create_list(self):
        for i in range(len(self.ifls)):
            if self.entrepots[i]==self.entrepot:
                self.L.append([self.ifls[i],self.prix[i],self.quantite[i],self.fournisseurs[i]])
                self.fournisseurs_set.add((self.fournisseurs[i],self.code[i]))
        self.pas=len(self.L)


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
                for i in range(3):
                    try:
                        h = self.browser.execute_script("return document.getElementsByClassName('NGREEN');")[26+i]
                        int(h.text)
                        return h.text
                    except:
                        if i==2:return None
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
        time.sleep(0.2)
        while True:
            time.sleep(0.1)
            try:
                h = self.browser.execute_script("return document.getElementById('sb_status');")
                if not "X SYSTEM" in h.text:
                    time.sleep(0.2)
                    break
            except:
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
        if self.get_first_imported()!=ifls:return True
        self.tab(9)
        self.write("1")
        self.enter()
        self.waiting_system()
        self.enter()
        self.waiting_system()
        self.action.send_keys(Keys.F3)
        self.action.perform()
        if ifls!=self.get_first_item():
            print("Product Not imported")
            return True
        else:
            print("Product Imported")
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
    
    def start(self,L):
        i=0
        #f1_system()
        while i<len(L):
            print(f"{i}: {L[i]}")
            #f1_system()
            self.waiting_system()
            self.suppr(6)
                
            self.ifls_input(L[i][0])
            if L[i][0]==self.get_first_item():
                print("Same")
            else:
                print("Not the same")
                #f1_system()
                if self.import_ifls(L[i][0]):
                    new_ifls=input("New ifls: ")
                    L[i][0]=f(new_ifls)
                    self.f1_system()
                    continue
            self.qp_input(str(L[i][2]),str(L[i][1]))
            i+=1
            self.ps+=1
    def init(self,L):
        #f1_system()
        self.action.send_keys(Keys.F6)
        self.action.perform()
        self.waiting_system()
        self.tab(1)
        self.write(L[0][3])
        if len(L[0][3])<=5:self.tab(1)
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
        for fournisseur in self.fournisseurs_set:
            #fournisseur=input("Saisir lefournisseur: ")
            L=filter(lambda x:fournisseur[0]==x[-1],self.L)
            L=set(L)
            if len(L)==0:continue
            time.sleep(1)
            self.init(L)
            self.waiting_system()
            self.start(L)
            self.write(Keys.F3)
            self.waiting_system()
            self.write(Keys.F3)
            self.waiting_system()