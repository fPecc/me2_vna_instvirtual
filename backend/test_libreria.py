from UTN_Keysight_9917A import VNA

miVNA = VNA("TCPIP::10.128.0.206::inst0::INSTR")

print(miVNA.Errcheck())

