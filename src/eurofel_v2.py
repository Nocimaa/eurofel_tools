#%%
#Faire le rapport un jours aussi mdrrrrr



import tkinter
import customtkinter
from PIL import Image
import selenium.webdriver
from fournisseur import Fournisseur
from magasin import Magasin
from tarif import Tarif
from facturation import Facturation
from credentials import Credentials
from pandas import read_excel
import os
import threading
from verif import License
if os.name == 'nt': from subprocess import CREATE_NO_WINDOW
#Main Windows
#Frame
class CredentialsFrame(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        customtkinter.CTkLabel(self,text='Chargement des logins...',text_color='white').pack()
        self.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
        
    def process(self):
        if self.master.credentials.fileExist():
            self.master.credentials.getCred()
            self.destroy()
            self.master.cred_ok()
        else:
            self.winfo_children()[-1].destroy()
            customtkinter.CTkEntry(self, placeholder_text="Username").pack(side='top',pady=(5,5))
            customtkinter.CTkEntry(self, placeholder_text="First Password").pack(side='top',pady=(5,5))
            customtkinter.CTkEntry(self, placeholder_text="Second Password").pack(side='top',pady=(5,5))
            customtkinter.CTkEntry(self, placeholder_text="Facturation Password").pack(side='top',pady=(5,5))
            customtkinter.CTkButton(self, text="Valider", command=self.register).pack(side='top',pady=(5,5))
    
    def register(self):
        username = self.winfo_children()[0].get()
        firstpasswd = self.winfo_children()[1].get()
        secondpasswd = self.winfo_children()[2].get()
        factpass = self.winfo_children()[3].get()
        self.master.credentials.setCred(username, firstpasswd, secondpasswd, factpass)
        self.master.credentials.getCred()
        self.destroy()
        self.master.cred_ok()


    
class LaunchFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master=master
        self.img=[Image.open("./excel.ico")]
        
        
        #Excel Image
        image = customtkinter.CTkImage(self.img[0],size=(50,50))
        customtkinter.CTkLabel(self,image=image,text="").pack(pady=(0,25), expand=True)
        #Excel Button

        customtkinter.CTkComboBox(self, values=["Rungis", "Marseille"]).pack(side='bottom')

        clickable = "normal" if self.master.validation[0] else "disabled"
        text_click = "Charger Excel" if self.master.validation[0] else "Désactivé"


        customtkinter.CTkButton(self,text=text_click,command=self.master.loadExcel, state=clickable).pack(side="bottom",pady=(25,25))

        #Excel Text
        customtkinter.CTkLabel(self,text="Not Loaded",text_color="red").pack(side="top")



        self.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
    

    def start_verify(self):self.master.verify()
    def invert_excel_text(self):
        if (type(self.master.my_frame) != LaunchFrame):
            return
        if self.master.file!=None:
            self.winfo_children()[3].configure(text="Loaded",text_color="green")
            self.master.launch_stated = True
        else:
            self.winfo_children()[3].configure(text_color="red",text="Not Loaded")
            #self.after(2000,self.invert_excel_text)


    #Will verify the excel
    def verify_excel(self):
        pass


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self.master=master
        self.p = []
        self.t = []
        self.started=False
        self.allprocess = True

        customtkinter.CTkLabel(self,text="Appuyer sur démarer pour lancer le processus").pack(side="top",pady=(25,25))
        customtkinter.CTkButton(self,text="Démarrer",width=150,height=40,command=lambda :self.configure()).pack()
        customtkinter.CTkLabel(self,text_color="red",text="").pack(side="bottom")
        if self.master.type =='FOURNISSEUR':
            liste = []
            if self.master.validation[1]: liste.append("Ferme") ; liste.append("Fictive")
            if self.master.validation[2]: liste.append("Tarif - Hyper / Dépannage") ;  liste.append("Tarif - Proxy") ;  liste.append("Tarif - Market")

            if len(liste) == 0: liste.append("Aucune module autorisé")

            customtkinter.CTkComboBox(self, values=liste).pack(pady=(20,20))
        else:

            liste = []
            
            if self.master.validation[3]: liste.append("Magasin")
            if self.master.validation[4]: liste.append("Facturation")

            if len(liste) == 0: liste.append("Aucune module autorisé")


            customtkinter.CTkComboBox(self, values=liste).pack(pady=(20,20))
        self.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)


    def configure(self):
        

        entrepot=set(self.master.excel['ENTREPOT'])
        self.excel_list=[]
        for e in entrepot:
            self.excel_list.append((self.master.excel[self.master.excel['ENTREPOT']==e],e))  
        
        self.commande_type = self.winfo_children()[-1].get()
        
        if self.commande_type == "Aucune module autorisé":
            return

        for e in self.excel_list:
            if self.master.type=='FOURNISSEUR':
                if self.commande_type == "Tarif - Proxy":
                    self.p.append(Tarif(self.master.excel,e[1], "R"))
                elif self.commande_type == "Tarif - Market":
                    self.p.append(Tarif(self.master.excel,e[1], "M"))
                elif self.commande_type == "Tarif - Hyper / Dépannage":
                    self.p.append(Tarif(self.master.excel,e[1], "0"))
                else:
                    self.p.append(Fournisseur(self.master.excel,e[1], self.master.geo))
                    self.p[-1].ffi = self.commande_type
            if self.master.type=='MAGASIN':
                if self.commande_type == "Magasin":
                    self.p.append(Magasin(self.master.excel,e[1]))
                else:
                    self.p.append(Facturation(self.master.excel, e[1], self.master.geo))
        self.switch()
        
    def switch(self):
        self.destroy()

        self.f2 = customtkinter.CTkFrame(self.master)
        entrepot_str="/".join([pro.entrepot for pro in self.p])
        self.el = customtkinter.CTkLabel(self.f2,text=f"Entrepot: {entrepot_str}").pack(side="left",padx=(75,75))
        self.sl = customtkinter.CTkLabel(self.f2,text=f"Secteur: {self.p[0].secteur}").pack(side="right",padx=(75,75))
        self.sl = customtkinter.CTkLabel(self.f2,text=f"Date: {self.p[0].date}").pack(padx=(75,75))
        self.f2.pack(pady=(25,25))

        
        self.f3 = customtkinter.CTkFrame(self.master)
        
        self.pas=sum([int(pro.pas) for pro in self.p])
        self.el=customtkinter.CTkLabel(self.f3,text=f"Produit à saisir: {self.pas}").pack(side="left",padx=(75,75))
        self.sl=customtkinter.CTkLabel(self.f3,text=f"Produit saisie: 0").pack(padx=(75,75))
        self.f3.pack(pady=(25,15))
        if self.commande_type == "Ferme" or self.commande_type == "Fictive":
            self.f4 = customtkinter.CTkFrame(self.master)
            customtkinter.CTkLabel(self.f4, text="Soft Warning: 0").pack(side="left",padx=(75,75))
            customtkinter.CTkLabel(self.f4, text="Hard Warning: 0").pack(padx=(75,75))
            self.f4.pack(pady=(15,25))
        self.but = customtkinter.CTkButton(self.master,text="Démarrer",command=lambda :self.get_start())
        self.but.place(relx=0.5,rely=0.6,anchor=tkinter.CENTER)


        self.pb=customtkinter.CTkProgressBar(self.master,width=600,height=25)
        self.pb.set(0)
        self.pb.place(relx=0.5,rely=0.8,anchor=tkinter.CENTER)

        self.refresh_status()

    def refresh_status(self):
        for el in self.p:
            if el.stopped != self.allprocess:
                if not self.allprocess:
                    self.but.configure(text="Démarrer")
                else:
                    self.but.configure(text="Arreter")
                break

        self.after(500, self.refresh_status)

    def get_start(self):
        self.allprocess = not self.allprocess
        if not self.p[0].stopped:
            self.but.configure(text="Démarrer")
        else:
            self.but.configure(text="Arreter")
        for process in self.p:
            process.stopped = not process.stopped

        if not self.started:
            self.started=True
            for process in self.p:
                self.th = threading.Thread(target=process.setup)
                self.t.append(self.th)
                self.th.start()
            self.update_pb()
            
            
    
    def update_pb(self):
        ps=sum([int(pro.ps) for pro in self.p])
        self.pb.set(ps/self.pas)
        self.f3.winfo_children()[-1].configure(text=f"Produit saisie: {ps}")
        if self.commande_type == "Ferme" or self.commande_type == "Fictive":
            sw=sum([int(pro.sw) for pro in self.p])
            hw=sum([int(pro.hw) for pro in self.p])
            self.f4.winfo_children()[0].configure(text=f"Soft Warning: {sw}")
            self.f4.winfo_children()[1].configure(text=f"Hard Warning: {hw}")

        self.after(2000,self.update_pb)
                                               

#Main Windows
class MainWindow(customtkinter.CTk):
    def __init__(self, value):
        super().__init__()

        self.validation = value

        self.geometry("800x400")
        customtkinter.set_appearance_mode("Dark")
        self.title("EuroFel Utility")
        
        self.file=None
        self.excel=None
        self.type=''
        self.credentials = Credentials() 
        self.launch_stated=False
        self.my_frame = CredentialsFrame(self)
        
        self.my_frame.process()
    
    def verify_ok(self):
        self.my_frame = CredentialsFrame(self)
        self.my_frame.process()
    def cred_ok(self):
        #destroy verify frame here
        self.my_frame = LaunchFrame(self, width=500)
        self.my_frame.start_verify()
        
    def loadExcel(self):
        try:self.file=tkinter.filedialog.askopenfile(title="Select excel file",initialdir='./',filetypes=(("Excel files", ".xlsx .xls"),))
        except: return
        try:self.excel=read_excel(self.file.name, sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':int,'FOURNISSEUR':str,'DATE':str,'JOUR':str,'CANAL':str,'MAGASIN':str, 'PC':str, 'PVC':str})
        except: return
        try:
            self.excel['DATE']
            self.type='FOURNISSEUR'
            self.launch_stated=True
            self.excel['Status']=''
            self.excel['Warning']=''
            return
        except: pass
        try:
            self.excel['JOUR']
            self.type='MAGASIN'
            self.launch_stated=True
            self.excel['Warning']=''
            return
        except:pass
        self.excel=None
        self.file=None
    def verify(self):
        if self.launch_stated:
            self.geo = self.my_frame.winfo_children()[1].get()
            self.my_frame.destroy()
            self.my_frame=MainFrame(self)
            return
        
        if type(self.my_frame) != LaunchFrame:
            return
        self.my_frame.invert_excel_text()
        self.after(1000,self.verify)

import ssl
import urllib
ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://raw.githubusercontent.com/Nocimaa/eurofel_license/main/carrefour_license'
try:
    req = urllib.request.urlopen(url)
    bool_val = [val == "True" for val in str(req.read())[2:-1].split('\\n')[:-1]]
    print(bool_val)

    App = MainWindow(bool_val)
    App.mainloop()
except Exception as err:
    with open("crash.log", "a+") as f:
        f.write(" ".join(err.args)+"\n")


# %%
