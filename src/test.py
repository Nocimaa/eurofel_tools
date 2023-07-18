from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import pandas as pd
import keyboard
import time

browser = webdriver.Chrome()
browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")


file = input("Veuillez saisir nom du fichier: ")
df = pd.read_excel(file, sheet_name=0)
IFLS = df['IFLS']
ENTREPOT = df['ENTREPOT']
CODE_FOURNISSEUR = df['CODE FOURNISSEUR']
PRIX = df['PRIX']
QUANTITE = df['QUANTITE']
FOURNISSEUR=df['FOURNISSEUR']

Choix=729
def get_first_item():
    h = browser.execute_script("return document.getElementsByTagName('span');")
    return h[109].text
def waiting_system():
    while True:
        time.sleep(0.1)
        try:
            h = browser.execute_script("return document.getElementById('sb_status');")
            if "X SYSTEM" in h.text:
                print("X System")
            else:
                break
        except:
            pass
def f1_system():
    keyboard.wait("f1")
    while keyboard.is_pressed("f1"):pass
def f(s):
    if len(s)== 5:s='0'+s
    return s
def start():
    fournisseur=input("Saisir lefournisseur: ")
    L=[]
    for i in range(len(IFLS)):
        if ENTREPOT[i]==Choix and FOURNISSEUR[i] == fournisseur:L.append([f(str(IFLS[i])),PRIX[i],QUANTITE[i],CODE_FOURNISSEUR[i],FOURNISSEUR[i]])
    L.sort(key=lambda x: (x[-1],x[0]))
     
    curr=""
    pressed=False
    i=0
    while i<len(L):
        print(f"{i}: {L[i]}")
        #f1_system()
        waiting_system()
        for _ in range(6):keyboard.press("suppr")#optionnel
        keyboard.write(L[i][0],delay=0.5)
        
        keyboard.press("enter")
        waiting_system()
        #f1_system()
        
        num = get_first_item()
        print(num)
        if int(num)==int(L[i][0]):print("same")
        else:print("not the same");f1_system()
        
        for _ in range(5):keyboard.press('tab')
        
        for _ in range(7):keyboard.press("suppr")
        keyboard.write(f"{L[i][2]}",delay=0.5)
        for _ in range(2):keyboard.press('tab')
        for _ in range(10):keyboard.press("suppr")
        keyboard.write(f"{L[i][1]}",delay=0.5)
        keyboard.press("enter")
        i+=1
while True:
    start()
print("Fin de processus")

#Recupere le X system (peut crash sur certaine page car pas de sb_status
"""
def waiting_system():
    while True:
        time.sleep(0.1)
        try:
            h = browser.execute_script("return document.getElementById('sb_status');")
            if "X SYSTEM" in h.text:
                print(h.text)
                break
        except:
            pass
"""

