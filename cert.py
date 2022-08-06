#Certificate class
#USAGE: serial # (unique), issuer ID, subject ID, subject public key

class certificate:
    def __init__(self, serial, is_id, sj_id, sj_PK):
        self.serial = serial
        self.is_id = is_id
        self.sj_id = sj_id
        self.sj_PK = sj_PK

    #Getters
    def getSerial(self):
        return self.serial

    def getIsId(self):
        return self.is_id

    def getSjId(self):
        return self.sj_id

    def getSjPk(self):
        return self.sj_PK

    #No Setters, as we want the CA to be the only entitiy which can
    #create certificates, and they are immutable for security




