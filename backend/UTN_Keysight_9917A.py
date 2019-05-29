import visa

class VNA:
    def __init__(self,connectionString):
        if connectionString == "Debug":
            print ("----------------------------------------")
            print ("Starting in Debug mode!")
            print ("----------------------------------------")
            self.debug = True
        else:
            rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
            self.myFieldFox = rm.open_resource(connectionString)
            self.debug = False
        

    def getBatteryCharge(self):
        if not self.debug:
            self.myFieldFox.write("SYST:BATT:ABSC?")
            ret = self.myFieldFox.read()
        else:
            ret = 98
        return ret

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