#%%
from selenium.webdriver.common.keys import Keys
import time
import credentials


def checkStop(f):
    def wrapper(*args):
        while args[0].stopped:
            time.sleep(0.5)
        return f(*args)
    return wrapper

class Abstract:

    def __init__(self) -> None:
        self.credentials = credentials.Credentials()
        self.stopped = True

    @checkStop
    def enter(self):
        self.action.send_keys(Keys.ENTER)
        self.action.perform()
        self.waiting_system()
    @checkStop
    def tab(self,i):
        for _ in range(i):self.action.send_keys(Keys.TAB)
        self.action.perform()
    @checkStop
    def suppr(self,i):
        for _ in range(i):self.action.send_keys(Keys.DELETE)
        self.action.perform()
    @checkStop
    def write(self,text):
        self.action.send_keys(str(text))
        self.action.perform()
    
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
    def loggin(self):
        self.write(self.credentials.username)
        self.tab(1)
        self.write(self.credentials.passwd)
        self.enter()
        self.waiting_system()
        time.sleep(4)
        while self.verif()==0:
            self.enter()
            self.waiting_system()
        print(self.credentials.secndpasswd)
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

    def verif(self):
        h = self.browser.execute_script("return document.getElementsByClassName('RGREEN');")
        return len(h)
# %%
