import os

class Credentials:
    def __init__(self):
        self.username = ""
        self.passwd = ""
        self.secndpasswd = ""
        self.facturationpass = ""
        if self.fileExist():
            self.getCred()
    def fileExist(self):
        return os.path.exists("credentials.erfl")
    def getCred(self):
        file = open("credentials.erfl", "r")
        self.username = file.readline()
        self.passwd = file.readline()
        self.secndpasswd = file.readline()
        self.facturationpass = file.readline()
        file.close()
    def setCred(self, username, passwd, secndpasswd,factpass):
        file = open("credentials.erfl", "w")
        file.write(username+'\n'+ passwd+'\n'+secndpasswd+'\n'+factpass+'\n')
        file.close()
    def deleteCred(self):
        if self.fileExist():
            os.remove("credentials.erfl")
if __name__ == "__main__":
    c = Credentials()
    c.setCred("abcd","test","ok")
    c.deleteCred()
