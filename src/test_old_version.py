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
daterecp=input("Veuillez saisir la date de reception (DD/MM/YY): ")
df = pd.read_excel(file, sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':str,'FOURNISSEUR':str})
IFLS = df['IFLS']
ENTREPOT = df['ENTREPOT']
CODE_FOURNISSEUR = df['CODE FOURNISSEUR']
PRIX = df['PRIX']
QUANTITE = df['QUANTITE']
FOURNISSEUR=df['FOURNISSEUR']
fournisseurs=set(FOURNISSEUR)

Choix=input("Selectionner Entrepot")
Secteur=input("Selectionner Secteur")

def close():browser.close()
def enter():keyboard.press("enter")
def tab():keyboard.press("tab")
def suppr():keyboard.press("suppr")

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
def qp_input(q,p,delay):
    for _ in range(5):tab()
    for _ in range(7):suppr()
    keyboard.write(q,delay=delay)
    for _ in range(2):tab()
    for _ in range(10):suppr()
    keyboard.write(p,delay=delay)
    keyboard.press("enter")
    waiting_system()
    
def import_ifls(ifls,delay):
    #f1_system()
    keyboard.press("shift+f1")
    waiting_system()
    keyboard.release("shift")
    keyboard.press("f6")
    waiting_system()
    keyboard.press("tab")
    keyboard.press("f4")
    waiting_system()
    for _ in range(2):keyboard.press("tab")
    keyboard.write(ifls,delay=delay)
    keyboard.press("enter")
    waiting_system()
    if get_first_imported()!=ifls:return True
    for _ in range(9):keyboard.press("tab")
    keyboard.write("1",delay=delay)
    keyboard.press("enter")
    waiting_system()
    keyboard.press("enter")
    waiting_system()
    keyboard.press("f3")
    waiting_system()
    if ifls!=get_first_item():
        print("Product Not imported")
        return True
    else:
        print("Product Imported")
        return False
def ifls_input(ifls,delay):
    keyboard.write(ifls,delay=delay)
    while True:
        h = browser.execute_script("return document.getElementsByTagName('span');")[73].text
        if len(h.strip())==6:
           break
        time.sleep(0.1)
    keyboard.press("enter")
    waiting_system()
    if h!=ifls:
        print("incorrect ifls")
        #f1_system()
        ifls_input(ifls,delay)
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
        try:
            print(f"{i}: {L[i]}")
            #f1_system()
            waiting_system()
            for _ in range(6):keyboard.press("suppr")#optionnel
            
            ifls_input(L[i][0],delay)
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
            qp_input(str(L[i][2]),str(L[i][1]),delay)
            i+=1
        except:
            print("Process Interuted")
            f1_system()
def init(L,delay):
    #f1_system()
    keyboard.press("F6")
    waiting_system()
    keyboard.press("tab")
    keyboard.write(fourniformat(L[0][3]),delay=delay)
    if len(L[0][3])<=5:keyboard.press("tab")
    for _ in range(8):keyboard.press("suppr")
    keyboard.write(daterecp.replace("/",""),delay=delay)
    keyboard.press("tab")
    keyboard.press("tab")
    keyboard.write(str(Secteur),delay=delay)
    keyboard.press("enter")
    waiting_system()
    keyboard.press("enter")
    waiting_system()
    keyboard.press("F6")
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
