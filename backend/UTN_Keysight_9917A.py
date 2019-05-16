import visa

class VNA:
    def __init__(self,connectionString):
        rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
        self.myFieldFox = rm.open_resource(connectionString)

    def Errcheck(self):

        myError = []

        ErrorList = self.myFieldFox.query("SYST:ERR?").split(',')

        Error = ErrorList[0]

        if int(Error) == 0:

            print ("+0, No Error!")

        else:

            while int(Error)!=0:

                print ("Error #: " + ErrorList[0])

                print ("Error Description: " + ErrorList[1])

                myError.append(ErrorList[0])

                myError.append(ErrorList[1])

                ErrorList = self.myFieldFox.query("SYST:ERR?").split(',')

                Error = ErrorList[0]

                myError = list(myError)

        return myError