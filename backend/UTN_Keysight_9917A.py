import visa

class VNA:

    def __init__(self,connectionString):
        """Initialization function for the VNA class
        
        Arguments:
            connectionString {string} -- Connection string (extracted from Keysight Connection Expert)
        """

        if connectionString == "Debug":
            print ("----------------------------------------")
            print ("Starting in Debug mode!")
            print ("----------------------------------------")
            self.debug = True
        else:
            rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
            self.myFieldFox = rm.open_resource(connectionString)
            self.debug = False
        
    def getNumberOfTraces(self) -> int:
        """Gets the number of traces on the screen
        
        Returns:
            int -- Number of traces
        """

        if not self.debug:
            self.myFieldFox.write("CALC:PAR:COUN?")
            ret = self.myFieldFox.read()
        else:
            ret = 4
        return ret

    def setNumberOfTraces(self,numberOfTraces: int) -> None:
        """Sets the number of traces on the screen
        
        Arguments:
            numberOfTraces {int} -- Number of traces
        
        Returns:
            None
        """

        if not self.debug:
            self.myFieldFox.write("CALC:PAR:COUN " + str(numberOfTraces))

        return

    def selectTrace(self,trace: int) -> None:
        """Select (make active) the current trace
        
        Arguments:
            trace {int} -- [description]
        
        Returns:
            None -- [description]
        """

        if not self.debug:
            self.myFieldFox.write("CALC:PAR" + str(trace) + ":SEL")

        return

    def setCenterFrequency(self,centerFreq: int) -> None:
        """Set the center frequency of the trace
        
        Arguments:
            centerFreq {int} -- Center frequency
        
        Returns:
            None
        """

        if not self.debug:
            self.myFieldFox.write("SENS:FREQ:CENT " + str(centerFreq))

        return

    def setSpanFrequency(self,freqSpan: int) -> None:
        """Set the frequency span of the trace
        
        Arguments:
            freqSpan {int} -- Frequency span
        
        Returns:
            None
        """

        if not self.debug:
            self.myFieldFox.write("SENS:FREQ:SPAN " + str(freqSpan))
    
        return

    def setStartFrequency(self,startFreq: int) -> None:
        """Set the start frequency of the trace
        
        Arguments:
            startFreq {int} -- Start frequency
        
        Returns:
            None
        """

        if not self.debug:
            self.myFieldFox.write("SENS:FREQ:STAR " + str(startFreq))
            ret = self.myFieldFox.read()
        else:
            ret = 98
        return ret

    def setStopFrequency(self, stopFreq: int) -> None:
        """Set the stop frequency of the trace
        
        Arguments:
            stopFreq {int} -- Stop frequency
        
        Returns:
            None
        """

        if not self.debug:
            self.myFieldFox.write("SENS:FREQ:STOP " + str(stopFreq))
            ret = self.myFieldFox.read()
        else:
            ret = 98
        return ret

    def getCenterFrequency(self) -> int:
        """Query the center frequency of the trace
        
        Returns:
            int -- Center frequency in Hz
        """
        if not self.debug:
            self.myFieldFox.write("SENS:FREQ:CENT?")
            ret = self.myFieldFox.read()
        else:
            ret = 98
        return ret

    def getSpanFrequency(self) -> int:
        """Query the frequency span of the trace
        
        Returns:
            int -- Frequency span in Hz
        """
        if not self.debug:
            self.myFieldFox.write("SENS:FREQ:SPAN?")
            ret = self.myFieldFox.read()
        else:
            ret = 98
        return ret

    def getStartFrequency(self) -> int:
        """Query the start frequency of the trace
        
        Returns:
            int -- Start frequency in Hz
        """
        if not self.debug:
            self.myFieldFox.write("SENS:FREQ:STAR?")
            ret = self.myFieldFox.read()
        else:
            ret = 98
        return ret

    def getStopFrequency(self) -> int:
        """Query the stop frequency of the trace
        
        Returns:
            int -- Stop frequency in Hz
        """
        if not self.debug:
            self.myFieldFox.write("SENS:FREQ:STOP?")
            ret = self.myFieldFox.read()
        else:
            ret = 98
        return ret

    def getBatteryCharge(self) -> int:
        """Gets the battery charge of the equipment
        
        Returns:
            int -- Battery charge in percentage
        """

        if not self.debug:
            self.myFieldFox.write("SYST:BATT:ABSC?")
            ret = self.myFieldFox.read()
        else:
            ret = 98
        return ret

    def getRemainingRunTime(self) -> int:
        """Returns the minutes of run time remaining based on running average of current being used
        
        Returns:
            int -- Remaining run time in minutes
        """
        if not self.debug:
            self.myFieldFox.write("SYST:BATT:ARTT?")
            ret = self.myFieldFox.read()
        else:
            ret = 60
        return ret

    def getBatteryTemperature(self) -> int:
        """Reads the current battery temperature
        
        Returns:
            int -- Battery temperature in Celsius
        """
        if not self.debug:
            self.myFieldFox.write("	SYST:BATT:TEMP?")
            ret = self.myFieldFox.read()
        else:
            ret = 60
        return ret

    def Errcheck(self) -> list:
        """Gets the list of errors of the equipment
        
        Returns:
            list -- List of errors
        """

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