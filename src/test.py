from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import pandas as pd
import keyboard
import time
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")
browser.creationflags = CREATE_NO_WINDOW
action=ActionChains(browser)

file = input("Veuillez saisir nom du fichier: ")
daterecp=input("Veuillez saisir la date de reception (DD/MM/YY): ")
df = pd.read_excel(file, sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':str,'FOURNISSEUR':str})
IFLS = df['IFLS']
ENTREPOT = df['ENTREPOT']
CODE_FOURNISSEUR = df['CODE FOURNISSEUR']
PRIX = df['PRIX']
QUANTITE = df['QUANTITE']
FOURNISSEUR=df['FOURNISSEUR']
fournisseurs=set(FOURNISSEUR)

Choix=input("Selectionner Entrepot: ")
Secteur=input("Selectionner Secteur: ")

def close():browser.close()
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
    

def get_first_item():
    while True:
        try:
            time.sleep(0.25)
            for i in range(3):
                try:
                    h = browser.execute_script("return document.getElementsByClassName('NGREEN');")[26+i]
                    int(h.text)
                    return h.text
                except:
                    if i==2:return None
        except:
            print("get_first crash")
            time.sleep(1)
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
    return None
def waiting_system():
    time.sleep(0.2)
    while True:
        time.sleep(0.1)
        try:
            h = browser.execute_script("return document.getElementById('sb_status');")
            if "X SYSTEM" in h.text:
                print("X System")
            else:
                time.sleep(0.2)
                break
        except:
            print("ah une erreur")
            time.sleep(1)
def qp_input(q,p):
    tab(5)
    suppr(7)
    write(q)
    tab(2)
    suppr(10)
    write(p)
    enter()
    waiting_system()
    
def import_ifls(ifls,delay):
    #f1_system()
    action.key_down(Keys.SHIFT).send_keys(Keys.F1).key_up(Keys.SHIFT)
    action.perform()
    waiting_system()
    action.send_keys(Keys.F6)
    action.perform()
    waiting_system()
    action.send_keys(Keys.TAB)
    action.perform()
    waiting_system()
    action.send_keys(Keys.F4)
    action.perform()
    waiting_system()
    tab(2)
    write(ifls)
    enter()
    waiting_system()
    if get_first_imported()!=ifls:return True
    tab(9)
    write("1")
    enter()
    waiting_system()
    enter()
    waiting_system()
    action.send_keys(Keys.F3)
    action.perform()
    if ifls!=get_first_item():
        print("Product Not imported")
        return True
    else:
        print("Product Imported")
        return False
def ifls_input(ifls):
    #f1_system()
    suppr(6)
    write(ifls)
    enter()
    waiting_system()
def f1_system():
    keyboard.wait("f1")
    while keyboard.is_pressed("f1"):pass
def f(s):
    if len(s)== 5:s='0'+s
    return s
def fourniformat(s):
    if len(s)<5:s="0"*(5-len(s))+s
    return s
def start(delay,L):
    i=0
    #f1_system()
    while i<len(L):
        print(f"{i}: {L[i]}")
        #f1_system()
        waiting_system()
        for _ in range(6):keyboard.press("suppr")#optionnel
            
        ifls_input(L[i][0])
        if L[i][0]==get_first_item():
            print("Same")
        else:
            print("Not the same")
            #f1_system()
            if import_ifls(L[i][0],delay):
                new_ifls=input("New ifls: ")
                L[i][0]=f(new_ifls)
                f1_system()
                continue
        qp_input(str(L[i][2]),str(L[i][1]))
        i+=1
def init(L,delay):
    #f1_system()
    action.send_keys(Keys.F6)
    action.perform()
    waiting_system()
    tab(1)
    write(L[0][3])
    if len(L[0][3])<=5:tab(1)
    suppr(8)
    write(daterecp.replace("/",""))
    tab(2)
    write(Secteur)
    enter()
    waiting_system()
    enter()
    waiting_system()
    action.send_keys(Keys.F6)
    action.perform()
    waiting_system()
delay=0.2
f1_system() 
for fournisseur in fournisseurs:
    #fournisseur=input("Saisir lefournisseur: ")
    L=[]
    for i in range(len(IFLS)):
        if ENTREPOT[i]==Choix and FOURNISSEUR[i] == fournisseur:L.append([f(str(IFLS[i])),PRIX[i],QUANTITE[i],str(CODE_FOURNISSEUR[i]),FOURNISSEUR[i]])
    L.sort(key=lambda x: (x[-1],x[0]))
    if len(L)==0:continue
    time.sleep(1)
    init(L,delay)
    waiting_system()
    start(delay,L)
    keyboard.press("f3")
    waiting_system()
    keyboard.press("f3")
    waiting_system()
    
print("Fin de processus")

def close():
    browser.close()
