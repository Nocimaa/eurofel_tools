#%%
#Faire le rapport un jours aussi mdrrrrr



import tkinter
import customtkinter
from PIL import Image
from fournisseur import Fournisseur
from magasin import Magasin
from tarif import Tarif
from pandas import read_excel,concat,ExcelWriter
import os
import threading
from verif import License
if os.name == 'nt': from subprocess import CREATE_NO_WINDOW
#Main Windows
#Frame
class VerifFrame(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.verif=None
        self.license = License()
        self.f1=customtkinter.CTkFrame(self)
        customtkinter.CTkLabel(self.f1,text='Vérification de license en cours...').pack()
        self.f1.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
        
        
        
    def start_process(self):
        self.process()
       
    def process(self):
        self.license.open_license()
        if self.license.valid:
            self.destroy()
            self.master.verify_ok()
        else:
            self.f1.winfo_children()[-1].destroy()
            customtkinter.CTkLabel(self.f1,text='Veuillez écrire la license.').pack(side='top',pady=(5,5))
            customtkinter.CTkLabel(self.f1,text='Format: 1234-5678-ABCD-EFGH').pack(side='top',pady=(5,10))
            customtkinter.CTkEntry(self.f1,width=250).pack(side='top',pady=(10,10))
            customtkinter.CTkButton(self.f1,text='Valider',command=self.validate_license).pack(side='bottom')

    def validate_license(self):
        license = self.f1.winfo_children()[2].get()
        if self.license.check_license(license):
            self.license.set_license(license)
            self.destroy()
            self.master.verify_ok()
        else:
            if not isinstance(self.f1.winfo_children()[-1],customtkinter.CTkLabel):
                customtkinter.CTkLabel(self.f1,text='License Incorrecte').pack(side='top',pady=(5,5))    
    
class LaunchFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master=master
        self.img=[Image.open("img/excel.ico")]
        
        
        #Excel Image
        self.ce = customtkinter.CTkImage(self.img[0],size=(50,50))
        self.cle=customtkinter.CTkLabel(self,image=self.ce,text="").pack(pady=(0,25))
        #Excel Button
        self.eb=customtkinter.CTkButton(self,text="Load Excel",command=lambda :self.master.loadExcel()).pack(side="bottom",pady=(25,25))
        #Excel Text
        self.et = customtkinter.CTkLabel(self,text="Not Loaded",text_color="red").pack(side="bottom")
        
        self.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
    

    def start_verify(self):self.master.verify()
    def invert_excel_text(self):
        if self.master.file!=None:
            self.winfo_children()[-1].configure(text="Loaded",text_color="green")
            self.master.launch_stated = True
        else:
            self.winfo_children()[-1].configure(text_color="red",text="Not Loaded")
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
     
     
        self.f1 = customtkinter.CTkFrame(master)
        self.lab=customtkinter.CTkLabel(self.f1,text="Appuyer sur demmarer pour lancer le processus").pack(side="top",pady=(25,25))
        self.but=customtkinter.CTkButton(self.f1,text="Démarrer",width=150,height=40,command=lambda :self.configure()).pack()
        self.lab2=customtkinter.CTkLabel(self.f1,text_color="red",text="").pack(side="bottom")
        if self.master.type =='FOURNISSEUR':
            self.td=customtkinter.CTkComboBox(self.f1, values=["Ferme", "Fictive","Tarif"]).pack(pady=(20,20))
        self.f1.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)


    def configure(self):
        

        entrepot=set(self.master.excel['ENTREPOT'])
        self.excel_list=[]
        for e in entrepot:
            self.excel_list.append((self.master.excel[self.master.excel['ENTREPOT']==e],e))  
        
        if self.master.type=='FOURNISSEUR':commande_type = self.f1.winfo_children()[-1].get()
        
        
        for e in self.excel_list:
            if self.master.type=='FOURNISSEUR':
                if commande_type == "Tarif":self.p.append(Tarif(e[0],e[1]))
                else:
                    self.p.append(Fournisseur(self.master.excel,e[1]))
                    self.p[-1].ffi = commande_type
            if self.master.type=='MAGASIN':self.p.append(Magasin(e[0],e[1]))
        self.switch()
        
    def switch(self):
        self.f1.destroy()

        self.f2 = customtkinter.CTkFrame(self.master)
        entrepot_str="/".join([pro.entrepot for pro in self.p])
        self.el=customtkinter.CTkLabel(self.f2,text=f"Entrepot: {entrepot_str}").pack(side="left",padx=(75,75))
        self.sl=customtkinter.CTkLabel(self.f2,text=f"Secteur: {self.p[0].secteur}").pack(side="right",padx=(75,75))
        self.sl=customtkinter.CTkLabel(self.f2,text=f"Date: {self.p[0].date}").pack(padx=(75,75))
        self.f2.pack(pady=(25,25))

        
        self.f3= customtkinter.CTkFrame(self.master)
        
        self.pas=sum([int(pro.pas) for pro in self.p])
        self.el=customtkinter.CTkLabel(self.f3,text=f"Produit à saisir: {self.pas}").pack(side="left",padx=(75,75))
        self.sl=customtkinter.CTkLabel(self.f3,text=f"Produit saisie: 0").pack(padx=(75,75))
        self.f3.pack(pady=(25,25))

        self.but = customtkinter.CTkButton(self.master,text="Démarrer",command=lambda :self.get_start())
        self.but.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

        self.pb=customtkinter.CTkProgressBar(self.master,width=600,height=25)
        self.pb.set(0)
        self.pb.place(relx=0.5,rely=0.8,anchor=tkinter.CENTER)

    def get_start(self):
        if self.started:
            self.but.configure(text="Démarrer")
            self.started=False
        else:
            self.but.configure(text="Arreter")
            #Appel fonction demmarage
            self.started=True
            for process in self.p:
                self.th = threading.Thread(target=process.setup)
                self.t.append(self.th)
                self.th.start()
            self.update_pb()
            
            #t = threading.Thread(target=self.writting_rapport)
            #t.start()
            
    
    def update_pb(self):
        
        ps=sum([int(pro.ps) for pro in self.p])
        self.pb.set(ps/self.pas)
        self.f3.winfo_children()[-1].configure(text=f"Produit saisie: {ps}")
        self.after(2000,self.update_pb)
                                               
        
#Main Windows
class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        customtkinter.set_appearance_mode("Dark")
        self.title("EuroFel Utility")
        
        self.file=None
        self.excel=None
        self.type=''
        
        self.launch_stated=False
        self.my_frame = VerifFrame(self)
        self.my_frame.start_process()
        
    def verify_ok(self):
        #destroy verify frame here
        self.my_frame = LaunchFrame(self)
        self.my_frame.start_verify()
        
    def loadExcel(self):
        try:self.file=tkinter.filedialog.askopenfile(title="Select excel file",initialdir='./',filetypes=(("Excel files", ".xlsx .xls"),))
        except:pass
        try:self.excel=read_excel(self.file.name, sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':str,'FOURNISSEUR':str,'DATE':str,'JOUR':str,'CANAL':str,'MAGASIN':str})
        except:pass
        self.excel['Status']=''
        try:
            self.excel['DATE']
            self.type='FOURNISSEUR'
            self.launch_stated=True
            return
        except:pass
        try:
            self.excel['JOUR']
            self.type='MAGASIN'
            self.launch_stated=True
            return
        except:pass
        self.excel=None
        self.file=None
    def verify(self):
        if self.launch_stated:
            self.my_frame.destroy()
            self.my_frame=MainFrame(self)
            return
        self.my_frame.invert_excel_text()
        self.after(1000,self.verify)
      

App = MainWindow()
App.mainloop()



# %%
