#import keyboard
from tkinter import filedialog
from pandas import read_excel
from openpyxl import load_workbook
import numpy as np

df = read_excel("carrefour.fournisseur.xlsx", sheet_name=0)
BASSIN=df['BASSIN']
IFLS = df['IFLS']
UL=df['UL']
ENTREPOT = df['ENTREPOT']
PRODUIT = df['PRODUIT']
CODE_FOURNISSEUR = df['CODE FOURNISSEUR']
PRIX = df['PRIX']
QUANTITE = df['QUANTITE']
FOURNISSEUR=df['FOURNISSEUR']

"""
Choix=729
def f(s):
    if len(s)== 5:s='0'+s
    return s
L=[]
for i in range(len(IFLS)):
    if ENTREPOT[i]==Choix:L.append([f(str(IFLS[i])),PRIX[i],QUANTITE[i],CODE_FOURNISSEUR[i],FOURNISSEUR[i]])
L.sort(key=lambda x: (x[-1],x[0]))

curr=""
pressed=False
i=0
while i<len(L):
    keyboard.wait("f1")
    while keyboard.is_pressed("f1"):pass
    print(f"{i}: {L[i]}")
    for _ in range(6):keyboard.press("delete")
    keyboard.write(L[i][0])
    keyboard.press("enter")
    keyboard.wait("f1")
    while keyboard.is_pressed("f1"):pass
    keyboard.write(f"\t\t\t\t\t")
    for _ in range(7):keyboard.press("delete")
    keyboard.write(f"L[i][2]\t\t")
    for _ in range(10):keyboard.press("delete")
    keyboard.write(f"{L[i][1]}")
    keyboard.press("enter")
    i+=1
"""

# %%
def load_excel():
    excel=filedialog.askopenfile(title="Select excel file",initialdir='./',filetypes=(('All files','*.*'),))
    df = read_excel("carrefour.fournisseur.xlsx", sheet_name=0)
    data=zip(df['BASSIN'],df['IFLS'],df['UL'],df['ENTREPOT'],df['PRODUIT'],df['CODE FOURNISSEUR'],df['PRIX'],df['QUANTITE'],df['FOURNISSEUR'])
    return data
