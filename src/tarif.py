#%%
import threading
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from pandas import read_excel

#%%

excel=read_excel("carrefour.fournisseur 020823 F.xlsx", sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':str,'FOURNISSEUR':str,'DATE':str,'UL':str})
service=ChromeService('chromedriver')
service.creation_flags= CREATE_NO_WINDOW
browser= webdriver.Chrome(service=service)
browser.minimize_window()
browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")

action = ActionChains(browser)

date="020823"
#%%
def enter():
        action.send_keys(Keys.ENTER)
        action.perform()
def tab(i):
    for _ in range(i):action.send_keys(Keys.TAB)
    action.perform()
def suppr(i):
    for _ in range(i):action.send_keys(Keys.DELETE)
    action.perform()
def write(text):
    action.send_keys(text)
    action.perform()
def waiting_system():
        time.sleep(0.1)
        while True:
            time.sleep(0.1)
            try:
                h = browser.execute_script("return document.getElementById('sb_status');")
                if not "X SYSTEM" in h.text:
                    break
            except:
                time.sleep(1)
        if  browser.execute_script("return document.getElementsByClassName('NWHITE');")[0].text.strip()=="Messages":
            enter()
            waiting_system()
        
def verif_tarif():
    while True:
        try:
            enter()
            waiting_system()
            if browser.execute_script("return document.getElementsByClassName('NWHITE');")[1].text=="MODIFICATION D'UN TARIF":
                return
        except:
            print("zeubi")
        
def get_first_imported():
    waiting_system()
    try:
        h = browser.execute_script("return document.getElementsByClassName('NGREEN');")[24]
        int(h.text)
        if len(h.text)!=6:raise ValueError
        return h.text
    except:
        pass
    try:
        h = browser.execute_script("return document.getElementsByClassName('NPINK');")[1]
        int(h.text)
        if len(h.text)!=6:raise ValueError
        return h.text
    except:
        pass
    print('Cannot be imported')


#%%
def tarif(excel):
    for i in range(10):
        cur = excel.iloc[i]
        write(date)
        tab(1)
        write(Keys.F4)
        waiting_system()
        tab(2)
        write(cur['IFLS'])
        enter()
        if get_first_imported()!= cur['IFLS']:
            write(Keys.F3)
            tab(5)
            continue
        tab(9)
        write('1')
        enter()
        waiting_system()
        tab(1)
        write('ONN')
        enter()
        waiting_system()
        enter()
        verif_tarif()
        enter()
        waiting_system()
        write(Keys.F3)
        waiting_system()
tarif(excel)
# %%
