#%%
from pandas import read_excel
import re
import json
excel=read_excel("carrefour.fournisseur.xlsx", sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':int,'FOURNISSEUR':str,'DATE':str,'JOUR':str,'CANAL':str,'MAGASIN':str})
with open("country.json", "r") as file:
    dic = json.loads(file.read())
#%%
vrac = r" Palox (\d+,?\d*) k?g | Vrac (\d+,?\d*) k?g | 1 rang (\d+,?\d*) k?g | Plateau (\d+,?\d*) k?g | Mini colis 1x(\d+,?\d*) k?g "
pcb = r" Plateau (\d+,?\d*) pcs - \d+,?\d* k?g | Barquettes (\d+,?\d*)x\d+,?\d* k?g | Vrac (\d+,?\d*) pcs - \d+,?\d* k?g | Filets (\d+,?\d*)x\d+,?\d* k?g | Bottes (\d+,?\d*)x(\d+,?\d*) k?g | - (\d+,?\d*)pcs - \d+,?\d* k?g | - (\d+,?\d*) pcs - \d+,?\d* k?g | Sachet (\d+,?\d*)x\d+,?\d* k?g | Vrac (\d+,?\d*)x\d+,?\d* k?g | Girsac (\d+,?\d*)x\d+,?\d* k?g "

re_vrac = re.compile(vrac)
re_pcb = re.compile(pcb)

def extract_tuple(match):
    return list(filter(lambda x : x != None, match))[0]

def check_warning(df):
    if df == "FRAIS LOGISTIQUE":
        return
    liste = excel.iloc[i]['PRODUIT'].split('/')
    origine = liste[-1].strip()

    #Get NGREEN
    #Get Origine

    #check origine

    for el in liste:
        match_vrac = re_vrac.match(el)
        if match_vrac != None:
            break
            #
        match_pcb = re_pcb.match(el)
        if match_pcb != None:
            break
            #
    else:
        print("Not Matched", liste)


for i in range(len(excel)):
    check_warning(excel.iloc[i]['PRODUIT'])
    continue

#%%
#%%