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

excel=read_excel("carrefour.magasin 050823.xlsx", sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'MAGASIN':str,'PRIX':str,'QUANTITE':str,'CANAL':str,'JOUR':str,'UL':str})
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
        time.sleep(0.2)
        while True:
            time.sleep(0.1)
            try:
                h = browser.execute_script("return document.getElementById('sb_status');")
                if not "X SYSTEM" in h.text:
                    time.sleep(0.2)
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
def create_fp(exc):
    cur = exc.iloc[0]
    write(Keys.F6)
    waiting_system()
    write(Keys.F4)
    waiting_system()
    tab(2)
    write(cur['IFLS'])
    enter()
    if get_first_imported() != cur['IFLS']:
        print("Cannot im", cur['IFLS'])
        write(Keys.F3)
        write(Keys.F3)
        return
        
    tab(9)
    write("1")
    enter()
    waiting_system()
    tab(2)
    write(cur['CANAL'])
    tab(1)
    suppr(8)
    write(cur['JOUR'])
    enter()
    waiting_system()
    enter()
    waiting_system()

t={"01593":10,"21290":3,"27778":10}

def input_market(exc):
    c=0
    t=dict(zip(exc['MAGASIN'],exc['QUANTITE']))
    while c != len(t.keys()):
        h=browser.execute_script("return document.getElementsByClassName('NGREEN');")
        tab(1)
        if int(h[23+7*11].text.strip())<int(min(t)):
            write(Keys.PAGE_DOWN)
            waiting_system()
            continue
        for i in range(12):
            if h[23+7*i].text.strip() in t.keys():
                write(t[h[23+7*i].text.strip()])
                c+=1
            if c==len(t.keys()):break
            tab(1)
        write(Keys.PAGE_DOWN)
        waiting_system()
    enter()
    waiting_system()
    write(Keys.F3)
    waiting_system()

def im(excel):
    
    for ifls in set(excel['IFLS']):
        exc=excel[excel['IFLS']==ifls].sort_values(by=['MAGASIN'],ascending=False)
        create_fp(exc)
        waiting_system()
        input_market(exc)
        waiting_system()


# %%
