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

    def getActualConfig(self) -> object:
        """Gets the actual configuration of the VNA screen
        
        Returns:
            object -- Object containing the configuration of the VNA screen
        """
        if not self.debug:#####################
            ntraces = myVNA.getNumberOfTraces()
            traces = []
            for i in range(1,ntraces+1)
                selectTrace(i)
                trace={
                        'number': i,
                        'xMin': getStartFrequency(),
                        'xMax': getStopFrequency(),
                        'yMin': getmindbm(),
                        'yMax': getmaxdbm(),
                        'xScale': getxscale(),
                        'yScale': getyscale(),
                        'type': getTypeFormat(),
                        'title': getTraceTitle(),
                        'xLabel': getxLabel(),
                        'yLabel': getyLabel()
                }
                traces.append(trace)  
            ret = {'traces': traces}
        else:
            trace1 = {
                        'number': 1,
                        'xMin': 100,
                        'xMax': 1000,
                        'yMin': 100,
                        'yMax': 1000,
                        'xScale': 'logarithmic',
                        'yScale': 'logarithmic',
                        'type': 'bode',
                        'title': 'S11',
                        'xLabel': 'xLabel1',
                        'yLabel': 'yLabel1'
                    }
            trace2 = {
                        'number': 2,
                        'xMin': 1,
                        'xMax': 100,
                        'yMin': 1,
                        'yMax': 1000,
                        'xScale': 'linear',
                        'yScale': 'linear',
                        'type': 'bode',
                        'title': 'S21',
                        'xLabel': 'xLabel1',
                        'yLabel': 'yLabel1'
                    }
            trace3 = {
                        'number': 3,
                        'xMin': 500,
                        'xMax': 10000,
                        'yMin': 100,
                        'yMax': 10000,
                        'xScale': 'linear',
                        'yScale': 'logarithmic',
                        'type': 'bode',
                        'title': 'S12',
                        'xLabel': 'xLabel1',
                        'yLabel': 'yLabel1'
                    }
            trace4 = {
                        'number': 4,
                        'xMin': 100,
                        'xMax': 10000,
                        'yMin': 500,
                        'yMax': 10000,
                        'xScale': 'logarithmic',
                        'yScale': 'linear',
                        'type': 'bode',
                        'title': 'S22',
                        'xLabel': 'xLabel1',
                        'yLabel': 'yLabel1'
                    }
            ret = {'traces': [ trace1, trace2, trace3, trace4 ]}
        return ret

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
            ret = 0
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
            ret = 1000000
        return ret

    def getmindbm(self) -> int:
        """Query the min power of the trace
        
        Returns:
            int -- min power in dbm
        """
        if not self.debug:
            # TODO: Buscar el comando correcto
            self.myFieldFox.write("")
            ret = self.myFieldFox.read()
        else:
            ret = -100
        return ret

    def getmaxdbm(self) -> int:
        """Query the max power of the trace
        
        Returns:
            int -- max power in dbm
        """
        if not self.debug:
            # TODO: Buscar el comando correcto
            self.myFieldFox.write("")
            ret = self.myFieldFox.read()
        else:
            ret = 0
        return ret

    def getxscale(self) -> int:
        """Query the xscale of the trace
        
        Returns:
            string -- linear/logaritmic scale (unit en mV/dB)
        """
        if not self.debug:
            # TODO: Verificar
            self.myFieldFox.write("TRAC:SPEC:AMPL:SCAL?")
            ret = self.myFieldFox.read()
        else:
            ret = 'LOG'
        return ret        

    def getyscale(self) -> int:
        """Query the yscale of the trace
        
        Returns:
            string -- linear/logaritmic scale (unit mV/dB)
        """
        if not self.debug:
            # TODO: Verificar
            self.myFieldFox.write("[:SENSe]:AMPLitude:SCALe?")
            ret = self.myFieldFox.read()
        else:
            ret = 'LOG'
        return ret        

    def getTypeFormat(self) -> int:
        """Query the format of the trace
        
        Returns:
            string -- linear/logaritmic scale (unit mV/dB)
        """
        if not self.debug:
            self.myFieldFox.write("CALC[:SEL]:FORM?")
            ret = self.myFieldFox.read()
        else:
            ret = 'LOG'
        return ret        

    def getTraceTitle(self) -> int:
        """Query the title of the trace
        
        Returns:
            string -- title of the trace
        """
        if not self.debug:
            # TODO: Verificar
            self.myFieldFox.write("DISPlay:TITLe:DATA?")
            ret = self.myFieldFox.read()
        else:
            ret = 'DEBUG MODE'
        return ret        

    def getxLabel(self) -> int:
        """Query the xlabel of the trace
        
        Returns:
            string -- title of the trace
        """
        if not self.debug:
            # TODO: Verificar
            self.myFieldFox.write("DISPlay:TITLe:DATA?")
            ret = self.myFieldFox.read()
        else:
            ret = 'xLabel'
        return ret        

    def getyLabel(self) -> int:
        """Query the ylabel of the trace
        
        Returns:
            string -- title of the trace
        """
        if not self.debug:
            # TODO: Verificar
            self.myFieldFox.write("DISPlay:TITLe:DATA?")
            ret = self.myFieldFox.read()
        else:
            ret = 'yLabel'
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