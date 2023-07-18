from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import pandas as pd
import keyboard
import time
from subprocess import CREATE_NO_WINDOW

browser = webdriver.Chrome()
browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")
browser.creationflags = CREATE_NO_WINDOW


file = input("Veuillez saisir nom du fichier: ")
df = pd.read_excel(file, sheet_name=0)
IFLS = df['IFLS']
ENTREPOT = df['ENTREPOT']
CODE_FOURNISSEUR = df['CODE FOURNISSEUR']
PRIX = df['PRIX']
QUANTITE = df['QUANTITE']
FOURNISSEUR=df['FOURNISSEUR']

Choix=729
def close():
    browser.close()
def get_first_item():
    while True:
        try:
            time.sleep(0.25)
            h = browser.execute_script("return document.getElementsByClassName('NGREEN');")[27]
            int(h.text)
            return h.text
        except:
            pass
def waiting_system():
    keyboard.press('enter')
    time.sleep(0.2)
    while True:
        time.sleep(0.1)
        try:
            h = browser.execute_script("return document.getElementById('sb_status');")
            if "X SYSTEM" in h.text:
                print("X System")
            else:
                time.sleep(0.1)
                break
        except:
            pass
def qp_input(q,p,delay):
    for _ in range(5):keyboard.press('tab')
    for _ in range(7):keyboard.press("suppr")
    keyboard.write(q,delay=delay)
    for _ in range(2):keyboard.press('tab')
    for _ in range(10):keyboard.press("suppr")
    keyboard.write(p,delay=delay)

    #keyboard.press("enter")
    waiting_system()
def import_ifls(ifls,delay):
    keyboard.press("f13")
    keyboard.press("f6")
    keyboard.press("tab")
    keyboard.press("f4")
    waiting_system()
    h = browser.execute_script("return document.getElementsByTagName('span');")[42].send_keys(ifls)
    keyboard.press("enter")
    for _ in range(9):keyboard.press("tab")
    time.sleep(0.5)
    keyboard.write("1")
    keyboard.press("enter")
    keyboard.press("enter")
    keyboard.press("f3")
    waiting_system()
    if ifls==get_first_item():
        print("IFLS imported")
    else:
        print("Problem")
        f1_system()
def ifls_input(ifls,delay):
    keyboard.write(ifls,delay=delay)
    while True:
        h = browser.execute_script("return document.getElementsByTagName('span');")[73].text
        if len(h.strip())==6:
           break
        time.sleep(0.1)
    #keyboard.press("enter")
    waiting_system()
    if h!=ifls:ifls_input(ifls,delay)
def f1_system():
    keyboard.wait("f1")
    while keyboard.is_pressed("f1"):pass
def f(s):
    if len(s)== 5:s='0'+s
    return s
def start(delay):
    fournisseur=input("Saisir lefournisseur: ")
    L=[]
    for i in range(len(IFLS)):
        if ENTREPOT[i]==Choix and FOURNISSEUR[i] == fournisseur:L.append([f(str(IFLS[i])),PRIX[i],QUANTITE[i],CODE_FOURNISSEUR[i],FOURNISSEUR[i]])
    L.sort(key=lambda x: (x[-1],x[0]))
     
    curr=""
    pressed=False
    i=0
    f1_system()
    while i<len(L):
        print(f"{i}: {L[i]}")
        #f1_system()
        waiting_system()
        for _ in range(6):keyboard.press("suppr")#optionnel
        #keyboard.write(L[i][0],delay=0.5)
        
        ifls_input(L[i][0],delay)
        if L[i][0]==get_first_item():
            print("Same")
        else:
            print("Not the same")
            import_ifls(L[i][0],delay)
        qp_input(str(L[i][2]),str(L[i][1]),delay)
        i+=1
while True:
    start(0.25)
print("Fin de processus")

#Recupere le X system (peut crash sur certaine page car pas de sb_status
def close():
    browser.close()
