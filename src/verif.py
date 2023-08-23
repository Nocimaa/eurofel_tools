#%%
import os

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
    
    def check_license(self):
        

k = License()
k.open_license()

# %%
