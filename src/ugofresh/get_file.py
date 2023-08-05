#%%
import requests
import datetime
import uncurl
#%%


s=requests.Session()
s.get("https://app.ugo-fresh.com/accounts/login/?next=%2Fmarket%2Fmy-offers")
csrf=s.cookies.get_dict()['csrftoken']

data = {"csrfmiddlewaretoken":csrf,"login":"dlahbib@hotmail.fr","password":"TANTAN78"}

s.post("https://app.ugo-fresh.com/accounts/login/?next=%2Fmarket%2Fmy-offers",allow_redirects=True,data=data)


date = ["09","10","2023","7","15"]
def get_str(d1,d2):
    f=f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={d1[2]}-{d1[1]}-{d1[0]}T{get_hour(d1[3])}%3A{get_minute(d1[4])}%3A00.000Z&datetime_to={d2[2]}-{d2[1]}-{d2[0]}T{get_hour(d2[3])}%3A{get_minute(d2[4])}%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805"

# %%
"""
f=https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from=2023-08-02T08%3A00%3A00.000Z&datetime_to=2023-08-03T08%3A00%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805


https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from=2023-08-02T09%3A00%3A00.000Z&datetime_to=2023-08-03T08%3A00%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805
https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from=2023-08-02T08%3A15%3A00.000Z&datetime_to=2023-08-03T08%3A03%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805


https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from=2023-08-02T08%3A00%3A00.000Z&datetime_to=2023-08-02T19%3A00%3A00.000Z&date_scope=order&state=accepted&template=carrefour.fournisseur.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805
"""

def get_year():
    return str(datetime.datetime.now().year)

def get_hour(h):
    h=int(h)
    h-=2
    if h<0:h+=24
    return "0"+str(h) if h<10 else str(h)
def get_minute(m):
    m=int(m)
    return "0"+str(m) if m<10 else str(m)



def get_proxy(date):
    st="".join(date)
    t=s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date[0]}-{date[1]}-{date[2]}T08%3A00%3A00.000Z&datetime_to={date[0]}-{date[1]}-{date[2]}T19%3A00%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
    
    open(f"carrefour.magasin.proxy {date[2]}{date[1]}{date[0][2:]}.xlsx","wb").write(t.content)
    
    t=s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date[0]}-{date[1]}-{date[2]}T08%3A00%3A00.000Z&datetime_to={date[0]}-{date[1]}-{date[2]}T19%3A00%3A00.000Z&date_scope=order&state=accepted&template=carrefour.fournisseur.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
    open(f"carrefour.fournisseur.proxy {date[2]}{date[1]}{date[0][2:]}.xlsx","wb")
    
def get_hyper(date):
    t=s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date[0]}-{date[1]}-{date[2]}T01%3A00%3A00.000Z&datetime_to={date[0]}-{date[1]}-{date[2]}T05%3A15%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
    
    open(f"carrefour.magasin.hyper {date[2]}{date[1]}{date[0][2:]}.xlsx","wb").write(t.content)
    
    t=s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date[0]}-{date[1]}-{date[2]}T01%3A00%3A00.000Z&datetime_to={date[0]}-{date[1]}-{date[2]}T05%3A15%3A00.000Z&date_scope=order&state=accepted&template=carrefour.fournisseur.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
    open(f"carrefour.fournisseur.hyper {date[2]}{date[1]}{date[0][2:]}.xlsx","wb")
def get_dep(date):
    pass
# %%
