#%%
import os
import datetime
#%%
class License():
    def __init__(self) -> None:
        self.license=''
        self.valid = False
        self.progress=0

    def open_license(self):
        if os.path.exists('settings.erfl'):
            with open('settings.erfl','r') as f: 
                self.license= f.read()
            self.check_license()
        else:
            with open('settings.erfl','w') as f:pass
            self.valid=False
    
    def write_license(self):
        with open('settings.erfl','w') as f:f.write(self.license)

    def set_license(self,license):
        self.license=license
        if self.check_license():
            self.write_license()


    def check_license(self,license=None):
        if license == None:license=self.license
        if len(license) == 19:
            date=self.decrypt(license)
            if date != None:
                now = datetime.datetime.now().date()
                if date>=now:
                    self.valid=True
                    return True
        self.valid=False
        return False


    def get_R(self,license):
        return (license[0],license[10],license[13])
    def get_E(self,license):
        return (license[1],license[7],license[8])
    def get_Y(self,license):
        return license[2]+license[6]+license[12]+license[15]
    def get_D(self,license):
        return license[3]+license[18]
    def get_M(self,license):
        return license[5]+license[11]
    def get_C(self,license):
        return license[-2]+license[-3]

    def decrypt(self,license):
        Y=self.get_Y(license)
        M=self.get_M(license)
        D=self.get_D(license)

        c='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        d1=dict()
        d2=dict()
        for i in range(len(c)):
            d1[c[i]]=i
            d2[str(i)]=c[i]

        E=[d1[el] for el in self.get_E(license)]
        R=[d1[el] for el in self.get_R(license)]
        Y=self.caesar(self.get_Y(license),d1,d2,-E[0]**R[0])
        M=self.caesar(self.get_M(license),d1,d2,-E[1]**R[1])
        D=self.caesar(self.get_D(license),d1,d2,-E[2]**R[2])

        try:
            return datetime.date(int(Y),int(M),int(D))
        except:
            return None
            
    def caesar(self,st,dict,dict1,key):
        s=''
        for e in st:
            k=str((dict[e]+key)%36)
            s+=dict1[k]
        return s

k = License()
k.open_license()

# %%
