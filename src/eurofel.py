#%%
import tkinter
import customtkinter
from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
from procedure import Procedure
from pandas import read_excel
from selenium.webdriver.chrome.service import Service as ChromeService
#from subprocess import CREATE_NO_WINDOW



#%%
#Main Windows
#Frame
class LaunchFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master=master
        #Chrome Button
        self.cb=customtkinter.CTkButton(master,text="Launch Chrome",command=lambda :self.master.launchBrowser())
        self.cb.place(relx=0.25,rely=0.6,anchor=tkinter.CENTER) 
        #Chrome and Excel Img
        self.img = [Image.open("img/chrome.ico"),Image.open("img/excel.ico")]
        
        self.ci = customtkinter.CTkImage(self.img[0],size=(50,50))
        self.clc=customtkinter.CTkLabel(master,image=self.ci,text="")
        self.clc.place(relx=0.25,rely=0.40,anchor=tkinter.CENTER)
        #Excel Text
        self.ct = customtkinter.CTkLabel(master,text="Not Launched",text_color="red")
        self.ct.place(relx=0.25,rely=0.75,anchor=tkinter.CENTER)
        

        #Excel Button
        self.eb=customtkinter.CTkButton(master,text="Load Excel",command=lambda :self.master.loadExcel())
        self.eb.place(relx=0.75,rely=0.6,anchor=tkinter.CENTER)
        #Excel Image
        self.ce = customtkinter.CTkImage(self.img[1],size=(50,50))
        self.cle=customtkinter.CTkLabel(master,image=self.ce,text="")
        self.cle.place(relx=0.75,rely=0.40,anchor=tkinter.CENTER)
        #Excel Text
        self.et = customtkinter.CTkLabel(master,text="Not Loaded",text_color="red")
        self.et.place(relx=0.75,rely=0.75,anchor=tkinter.CENTER)

    
        self.verify()
    def invert_chrome_text(self):
        try:
            self.master.browser.current_url
            self.ct.configure(text="Launched",text_color="green")
            return True
        except:
            self.ct.configure(text_color="red",text="Not Launched")
            return False

    def invert_excel_text(self):
        if self.master.file!=None:
            self.et.configure(text="Loaded",text_color="green")
        else:
            self.et.configure(text_color="red",text="Not Loaded")
        return True

    def verify(self):
        self.invert_excel_text()
        self.invert_chrome_text()
        self.after(1000,self.verify)

    def clear_frame(self):
        for el in self.master.winfo_children():
            el.destroy()

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self.master=master
        self.p = Procedure(master.browser,master.excel)
     
        self.f1 = customtkinter.CTkFrame(master)
        self.lab=customtkinter.CTkLabel(self.f1,text="Connectez-vous à un entrepot\nAller sur GESTION DES COMMANDES D'ACHATS\n(01->02->07)\nPuis appuyez sur configurer.").pack(side="top",pady=(25,25))
        self.but=customtkinter.CTkButton(self.f1,text="Configurer",width=150,height=40,command=lambda :self.configure()).pack()
        self.lab2=customtkinter.CTkLabel(self.f1,text_color="red",text="").pack(side="bottom")

        self.f1.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)


    def configure(self):
        if not self.p.get_Entrepot():
            self.f1.winfo_children()[-1].configure(text="Impossible de récupérer l'entrepot.")
            return
        if not self.p.get_date():
            self.f1.winfo_children()[-1].configuree(text="Impossible de charger la date sur l'excel.")
            return
        self.p.create_list()
        self.switch()
    def clear_frame(self):
        for el in self.master.winfo_children():
            el.destroy()
        self.destroy()

    def switch(self):
        self.f1.destroy()

        self.f2 = customtkinter.CTkFrame(self.master)
        self.el=customtkinter.CTkLabel(self.f2,text=f"Entrepot: {self.p.entrepot}").pack(side="left",padx=(75,75))
        self.sl=customtkinter.CTkLabel(self.f2,text=f"Secteur: {self.p.secteur}").pack(side="right",padx=(75,75))
        self.sl=customtkinter.CTkLabel(self.f2,text=f"Date: {self.p.date[:2]}/{self.p.date[2:4]}/{self.p.date[4:]}").pack(padx=(75,75))
        self.f2.pack(pady=(25,25))

        
        self.f3= customtkinter.CTkFrame(self.master)
        self.el=customtkinter.CTkLabel(self.f3,text=f"Produit à saisir: {self.p.pas}").pack(side="left",padx=(75,75))
        self.sl=customtkinter.CTkLabel(self.f3,text=f"Produit saisie: {self.p.ps}").pack(padx=(75,75))
        self.f3.pack(pady=(25,25))

        self.but = customtkinter.CTkButton(self.master,text="Démarrer",command=lambda :self.get_start())
        self.but.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

        self.pb=customtkinter.CTkProgressBar(self.master,width=600,height=25)
        self.pb.set(0)
        self.pb.place(relx=0.5,rely=0.8,anchor=tkinter.CENTER)

    def get_start(self):
        if self.p.start:
            self.but.configure(text="Démarrer")
            self.p.start=False
        else:
            self.but.configure(text="Arreter")
            self.p.start=True

#Main Windows
class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        customtkinter.set_appearance_mode("Dark")
        self.title("EuroFel Utility")
        self.browser=None
        self.file=None
        self.excel=None
        self.state=[False,False]
        self.my_frame = LaunchFrame(self)

        self.verify()

    
    def launchBrowser(self):
        self.browser=webdriver.Chrome()
        #self.browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")
        self.browser.get("https://www.google.com")
    def loadExcel(self):
        self.file=tkinter.filedialog.askopenfile(title="Select excel file",initialdir='./',filetypes=(("Excel files", ".xlsx .xls"),))
        self.excel=read_excel(self.file.name, sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':str,'FOURNISSEUR':str})
    def verify(self):
        if isinstance(self.my_frame,LaunchFrame):
            self.state[0]=self.my_frame.invert_excel_text()
            self.state[1]=self.my_frame.invert_chrome_text()

        try:self.browser.current_url;self.state[1]=True
        except:self.state[1]=False
        
        self.state[0]=self.file!=None

        if not False in self.state and isinstance(self.my_frame,LaunchFrame):
            self.my_frame.clear_frame()
            self.my_frame=MainFrame(self)
        if False in self.state and isinstance(self.my_frame,MainFrame):self.my_frame=LaunchFrame(self)

        self.after(1000,self.verify)

class Test(customtkinter.CTk):
    def __init__(self):
            super().__init__()
            self.geometry("800x400")
            self.title("EuroFel Utility")
            customtkinter.set_appearance_mode("Dark")

            #self.service=ChromeService('chromedriver')
            #self.service.creation_flags= CREATE_NO_WINDOW
            #self.browser= webdriver.Chrome(service=self.service)
            #self.browser= webdriver.Chrome()
            #self.browser.get("https://pace.fr.carrefour.com/eurofel/webaccess/")
            self.browser=None


            self.file="carrefour.fournisseur 270723 FI.xlsx"
            self.excel=read_excel(self.file, sheet_name=0,converters={'IFLS':str,'ENTREPOT':str,'CODE FOURNISSEUR':str,'PRIX':str,'QUANTITE':str,'FOURNISSEUR':str})
            self.stateeee=[False,False]
            self.p=None
            self.my_frame = MainFrame(self)   

App = MainWindow()
App.mainloop()
App.browser.close()




# %%
