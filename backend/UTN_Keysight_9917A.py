import visa
import uuid
from collections import deque
from threading import Timer

timeout = 60*5

class VNA:

    def __init__(self,connectionString):
        """Initialization function for the VNA class
        
        Arguments:
            connectionString {string} -- Connection string (extracted from Keysight Connection Expert)
        """
        # Users queue
        self.usersQueue = deque([])
        # User change timer
        self.timer = None
        self.timer = Timer(timeout,self.rotateUsers())

        if connectionString == "Debug":
            print ("----------------------------------------")
            print ("Starting in Debug mode!")
            print ("----------------------------------------")
            self.debug = True
        else:
            rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
            self.myFieldFox = rm.open_resource(connectionString)
            #self.myFieldFox.read_termination = '\n'
            self.myFieldFox.write_termination = '\n'
            # self.myFieldFox.timeout = 30000
            self.debug = False

    def getActualConfig(self) -> object:
        """Gets the actual configuration of the VNA screen
        
        Returns:
            object -- Object containing the configuration of the VNA screen
        """
        if not self.debug:
            ntraces = int(self.getNumberOfTraces())
            traces = []
            for i in range(1,ntraces+1):
                self.selectTrace(i)
                data = self.getData()
                trace={
                        'number': i,
                        'xMin': self.getStartFrequency(),
                        'xMax': self.getStopFrequency(),
                        'yMin': self.getmindbm(i),#min([x['y'] for x in data]), #getmindbm(),
                        'yMax': self.getmaxdbm(i),#max([x['y'] for x in data]), #getmaxdbm(),
                        'xScale': "linear",#self.getxscale()
                        'yScale': "linear",#self.getyscale(),
                        'type': "bode",#self.getTypeFormat(),
                        'title': self.getTraceTitle(i),
                        'xLabel': "Freq",#getxLabel(),
                        'yLabel': "dBm", #getyLabel()
                        'data': data,
                        'yPDiv': self.getYPDiv(i)
                }
                traces.append(trace)  
            ret = {
                'traces': traces, 
                'sweepResolution': self.getSweepResolution(),
                'IFBW': self.getIFBW() 
                }
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
                        'xLabel': 'Freq',
                        'yLabel': 'dBm',
                        'yPDiv': 10,
                        'data': [
                            {'x': 100,'y': 100},
                            {'x': 200,'y': 150},
                            {'x': 500,'y': 300},
                            {'x': 1000,'y': 800}
                            ]
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
                        'xLabel': 'Freq',
                        'yLabel': 'dBm',
                        'yPDiv': 10,
                        'data': [
                            {'x': 1,'y': 100},
                            {'x': 20,'y': 250},
                            {'x': 50,'y': 200},
                            {'x': 100,'y': 600}
                            ]
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
                        'xLabel': 'Freq',
                        'yLabel': 'dBm',
                        'yPDiv': 10,
                        'data': [
                            {'x': 500,'y': 100},
                            {'x': 2000,'y': 1000},
                            {'x': 5000,'y': 3000},
                            {'x': 10000,'y': 8000}
                            ]
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
                        'xLabel': 'Freq',
                        'yLabel': 'dBm',
                        'yPDiv': 10,
                        'data': [
                            {'x': 100,'y': 500},
                            {'x': 2000,'y': 5000},
                            {'x': 5000,'y': 2000},
                            {'x': 10000,'y': 4000}
                            ]
                    }
            ret = {
                'traces': [ trace1, trace2, trace3, trace4 ], 
                'sweepResolution': 401,
                'IFBW': 10000 
                }
        return ret

    def getYMin(self) -> int:
        self.myFieldFox.write("CALC:DATA:FDAT?")
        y = self.myFieldFox.read()
        y = y.split(",")
        return min(y)

    def getYMax(self) -> int:
        self.myFieldFox.write("CALC:DATA:FDAT?")
        y = self.myFieldFox.read()
        y = y.split(",")
        return max(y)

    def getData(self) -> object:
        self.myFieldFox.write("FREQ:DATA?")
        x = self.myFieldFox.read()
        x = x.split(",")
        self.myFieldFox.write("CALC:DATA:FDAT?")
        y = self.myFieldFox.read()
        y = y.split(",")
        data = []
        for i in range(1,len(x)):
            element = {
                'x': float(x[i]),
                'y': float(y[i])
            }
            data.append(element)
            print(x[i] + "/" + y[i])
        return data

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

    def setSweepResolution(self,sweepResolution: int) -> None:
        """Sets the sweep resolution points of the instrument
        
        Arguments:
            sweepResolution {int} -- Sweep resolution to set
        
        Returns:
            None
        """

        if not self.debug:
            self.myFieldFox.write("SWE:POIN " + str(sweepResolution))

        return

    def setSweepTime(self,sweepTime: float) -> None:

        if not self.debug:
            self.myFieldFox.write("SWE:TIME " + str(sweepTime))

        return

    def getSweepTime(self) -> int:

        if not self.debug:
            self.myFieldFox.write("SWE:TIME?")
            ret = self.myFieldFox.read()
        else:
            ret = 1
        return ret

    def getSweepResolution(self) -> int:
        """Gets the sweep resolution points of the instrument
        
        Returns:
            int -- resolution points
        """

        if not self.debug:
            self.myFieldFox.write("SWE:POIN?")
            ret = int(self.myFieldFox.read())
        else:
            ret = 401
        return ret

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
            ret = int(self.myFieldFox.read())
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
            ret = int(self.myFieldFox.read())
        else:
            ret = 1000000
        return ret

    def setIFBW(self, ifBW: int) -> None:
        """Sets the IFBW of the VNA
        
        Arguments:
            ifBW {int} -- IFBW to be set
        
        Returns:
            None -- 
        """

        if not self.debug:
            self.myFieldFox.write("SENS:BWID " + str(ifBW))

        return 

    def getIFBW(self) -> int:
        """Query the IFBW of the VNA
        
        Returns:
            int -- IFBW
        """
        if not self.debug:
            self.myFieldFox.write("SENS:BWID?")
            ret = int(self.myFieldFox.read())
        else:
            ret = 1000000
        return ret

    def getmindbm(self, trace: int) -> int:

        if not self.debug:
            self.myFieldFox.write("DISP:WIND:TRAC"+str(trace)+":Y:BOTT?")
            ret = float(self.myFieldFox.read())
        else:
            ret = -100
        return ret

    def getmaxdbm(self,trace: int) -> int:

        if not self.debug:
            self.myFieldFox.write("DISP:WIND:TRAC"+str(trace)+":Y:TOP?")
            ret = float(self.myFieldFox.read())
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

    def getYPDiv(self, trace: int) -> int:
        if not self.debug:
            self.myFieldFox.write("DISP:WIND:TRAC"+str(trace)+":Y:PDIV?")
            ret = int(self.myFieldFox.read())
        else:
            ret = 10
        return ret

    def getyscale(self, trace: int) -> str:
        """Query the yscale of the trace
        
        Returns:
            str -- linear/logaritmic scale (unit mV/dB)
        """        
        if not self.debug:
            # TODO: Verificar
            #self.myFieldFox.write("[:SENSe]:AMPLitude:SCALe?")
            #self.myFieldFox.write("SENS:AMPL:SCAL?")
            self.myFieldFox.write("CALC1:FORM?")
            ret = self.myFieldFox.read()
            if ret == "MLOG\n":
                ret = "logarithmic"
            elif ret == "MLIN\n":
                ret = "linear"
            else:
                ret = ""
        else:
            ret = 'logarithmic'
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

    def getTraceTitle(self, trace: int) -> str:
        """Query the title of the trace
        
        Returns:
            string -- title of the trace
        """
        if not self.debug:
            self.myFieldFox.write("DISP:MARK:LARG:A:DEF:TRAC"+str(trace)+":MEAS??")
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

    def addNewUser(self) -> str:
        """This function adds a user to the usersQueue
        
        Returns:
            str -- uuid of the added user
        """
        userId = str(uuid.uuid4())

        if len(self.usersQueue):
            # Start timer or logic to change user
            self.timer.start()

        self.usersQueue.append(userId)
        return userId

    def checkIfUserIsCurrent(self,userId : str) -> bool:
        """This function checks if the session user is the one with the mutex
        
        Arguments:
            userId {str} -- uuid of the user
        
        Returns:
            bool -- True: user is current
        """

        if userId == userId[0]:
            return True
        else:
            return False

    def rotateUsers(self) -> None:
        """Callback for the expiration of the timer
        
        Returns:
            None -- 
        """
        self.usersQueue.rotate(-1)
        if self.timer:
            self.timer.start()

    def deleteUser(self,uuid) -> None:
        self.usersQueue.remove(uuid)
