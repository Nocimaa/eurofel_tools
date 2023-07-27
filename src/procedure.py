import time
import threading






class Procedure():
    def __init__(self,browser,excel):
        self.browser = browser
        self.excel = excel

        self.entrepot=None
        self.secteur=None
        self.date=None
        self.fournisseurs_set=set()


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
        except: pass
        finally: return False
    
    def get_secteur(self):
        if self.entrepot == '175':self.secteur='12'
        else:self.secteur='2'
        return True
    def get_date(self):
        try:
            self.date=self.excel['DATE'][0]
            return True
        except:pass
        finally: return False
    
    def create_list(self):
        for i in range(len(self.ifls)):
            if self.entrepots==self.entrepot:
                self.L.append([self.ifls[i],self.prix[i],self.quantite[i],self.fournisseurs[i]])
                self.fournisseurs_set.add((self.fournisseurs[i],self.code[i]))
