#%%
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

#%%
driver = webdriver.Chrome()

#%%
driver.get("https://pace.fr.carrefour.com/eurofel/webaccess/")
action=ActionChains(driver)
#%%

credentials = ["FRUBY5G","Mathieu6"]


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


def loggin():
    write(credentials[0])
    tab(1)
    write(credentials[1])
    enter()
    waiting_system()
    while verif()==0:
        enter()
        waiting_system()
    write(credentials[0])
    enter()
    waiting_system()

def choose_bassin(bassin):
    if bassin=="901":
        tab(1)
    if bassin=="961":
        tab(2)
    write("1")
    enter()
    waiting_system()
    while verif()==0:
        enter()
        waiting_system()

def choose_entrepot(entrepot):
    write("07")
    write(entrepot)
    enter()
    waiting_system()
    tab(4)
    write("1")
    enter()
    waiting_system()
    
def verif():
    h = driver.execute_script("return document.getElementsByClassName('RGREEN');")
    return len(h)


def waiting_system():
        time.sleep(0.2)
        while True:
            time.sleep(0.1)
            try:
                h = driver.execute_script("return document.getElementById('sb_status');")
                if not "X SYSTEM" in h.text:
                    time.sleep(0.2)
                    break
            except:
                time.sleep(1)
                
def full_process(bassin,entrepot):
    loggin()
    choose_bassin(bassin)
    choose_entrepot(entrepot)
      
#%%
def magasin_input(l):
    i=0
    while i != len(l):
        h = driver.execute_script("return document.getElementsByClassName('NGREEN');")
        for j in range(12):
            tab(1)
            if h[23+i*7].text in l.keys():
                write(l[h[23+i*7]])
                i+=1