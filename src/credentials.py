import os

class Credentials:
    def __init__(self):
        self.username = ""
        self.passwd = ""
        self.secndpasswd = ""
    def fileExist(self):
        return os.path.exists("credentials.erfl")
    def getCred(self):
        file = open("credentials.erfl", "r")
        self.username = file.readline()
        self.passwd = file.dline()
        self.secndpasswd = file.readline()
        file.close()
    def setCred(self, username, passwd, secndpasswd):
        file = open("credentials.erfl", "w")
        file.write(username+'\n'+ passwd+'\n'+secndpasswd+'\n')
        file.close()
    def deleteCred(self):
        if self.fileExist():
            os.remove("credentials.erfl")
if __name__ == "__main__":
    c = Credentials()
    c.setCred("abcd","test","ok")
    c.deleteCred()
