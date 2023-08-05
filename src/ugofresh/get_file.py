#%%
import requests
import datetime
#%%
class UgoFresh():
    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.get("https://app.ugo-fresh.com/accounts/login/?next=%2Fmarket%2Fmy-offers")
        self.data = {"csrfmiddlewaretoken":self.s.cookies.get_dict()['csrftoken'],"login":"dlahbib@hotmail.fr","password":"TANTAN78"}
        self.s.post("https://app.ugo-fresh.com/accounts/login/?next=%2Fmarket%2Fmy-offers",allow_redirects=True,data=self.data)
        self.date = datetime.datetime.now()

    def str_format(self,s):
        s=str(s)
        if len(s)==1:return "0"+s
        if len(s)==4:return s[:2]
        return s


    def get_proxy(self):
        date=self.date-datetime.timedelta(days=1)  
        if date.weekday()!=6:
            file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T08%3A00%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T19%3A00%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
            open(f"carrefour.magasin.proxy {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
            file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T08%3A00%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T19%3A00%3A00.000Z&date_scope=order&state=accepted&template=carrefour.fournisseur.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
            open(f"carrefour.fournisseur.proxy {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
        else:
            print("TO DO")
    def get_hyper(self):
        date=self.date
        file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T01%3A00%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T05%3A15%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
        open(f"carrefour.magasin.hyper {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
        file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T01%3A00%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T05%3A15%3A00.000Z&date_scope=order&state=accepted&template=carrefour.fournisseur.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
        open(f"carrefour.fournisseur.hyper {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
    def get_dep(self):
        date=self.date
        file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T05%3A15%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T7%3A30%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
        open(f"carrefour.magasin.dep {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
        file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T05%3A15%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T7%3A30%3A00.000Z&date_scope=order&state=accepted&template=carrefour.fournisseur.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
        open(f"carrefour.fournisseur.dep {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)

# %%
