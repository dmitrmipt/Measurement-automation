import visa
from time import sleep

class Instr(object):

    def __str__(self):
        return self.visa_instr

    def __repr__(self):
        return self.visa_instr

    # def __new__(self):
    #     return self

    def __init__(self, visa_name):
        self.visa_name = visa_name
        self.visa_resource_manager = visa.ResourceManager()
        self.visa_instr = self.visa_resource_manager.open_resource(self.visa_name)
        self.visa_instr.timeout = 10000
        # self.visa_instr.values_format = "ascii"
        # self.visa_instr.lock = NI_NO_LOCK


    def idn(self):
        print(self.visa_instr.query("*IDN?"))

    def clear(self):
        self.visa_instr.clear()
        print("Instrument cleared.")

    def cls(self):
        # Clear the instrument's Status Byte
        self.visa_instr.write("*CLS")
        return "Status byte cleared (*CLS)."

    def get_control_port(self): # NOT NECESSARY IF USING GPIB OR LAN CONNEXION WITH VXI-11 INSTEAD OF SOCKETS
        bla = self.visa_instr.query("SYSTem:COMMunicate:TCPip:CONTrol?")
        try:
            output = int(bla)
        except:
            print("Error while getting control port: value returned: {0}".format(bla))
            output = -1
        return output

    def trigger(self):
        self.visa_instr.trigger()
        return "Trigger sent."

    def read(self):
        # print("Reading...")
        return self.visa_instr.read()

    def query(self, command):
        # print("Querying {0}...".format(command))
        return self.visa_instr.query(command)

    def write(self, command):
        # print("Writing {0}".format(command))
        self.visa_instr.write(command)

    def prepare_for_stb(self):
        # Clear the instrument's Status Byte
        self.cls()
        # Enable for the OPC bit (bit 0, which has weight 1) in the instrument's
        # Event Status Register, so that when that bit's value transitions from 0 to 1
        # then the Event Status Register bit in the Status Byte (bit 5 of that byte)
        # will become set.
        self.visa_instr.write("*ESE 1")
        return "OPC bit enabled (*ESE 1)."

    def prepare_for_srq(self):
        # Clear the instrument's Status Byte
        self.cls()
        # Enable for the OPC bit (bit 0, which has weight 1) in the instrument's
        # Event Status Register, so that when that bit's value transitions from 0 to 1
        # then the Event Status Register bit in the Status Byte (bit 5 of that byte)
        # will become set.
        self.visa_instr.write("*ESE 1")
        # Enable for bit 5 (which has weight 32) in the Status Byte to generate an
        # SRQ when that bit's value transitions from 0 to 1.
        self.visa_instr.write("*SRE 32")
        print("OPC bit enabled (*ESE 1). Enable generation of SRQ (*SRE 32).")

    def wait_opc(self):
        self.visa_instr.query("*OPC?")

    def wait_for_stb(self):
        self.visa_instr.write("*OPC")
        done = False
        while not(done):
            bla = self.visa_instr.query("*STB?")
            try:
                stb_value = int(bla)
            except:
                print("Error in wait(): value returned: {0}".format(bla))
            else:
                done = (2**5 == (2**5 & stb_value))
                sleep(0.01)

    def wait_for_srq(self): # ONLY WORKS WITH GPIB ! NOT TESTED !
        self.visa_instr.write("*OPC")
        self.visa_instr.wait_for_srq(10)
