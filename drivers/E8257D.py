import drivers.instr as instr


class MXG(instr.Instr):

    def __init__(self, ip_address):
        super(MXG, self).__init__(ip_address)
        # self.cls()

    def use_internal_clock(self, is_clock_internal):
        if is_clock_internal:
            self.write(":SOURce:ROSCillator:SOURce:AUTO OFF")
        else:
            self.write(":SOURce:ROSCillator:SOURce:AUTO ON")

    def set_output_state(self, output_state):
        '''
        "ON" of "OFF"
        '''
        self.write(":OUTput:STATe "+output_state)

    def get_output_state(self):
        return self.query(":OUTput:STATe?")

    def set_freq_mode_fixed(self):
        self.write(":SOURce:FREQuency:MODE FIXed")

    def set_power_mode_fixed(self):
        self.write(":SOURce:POWer:MODE FIXed")

    def set_frequency(self, freq):
        self.write(":SOURce:FREQuency:CW {0}HZ".format(freq))

    def get_frequency(self):
        bla = self.query(":SOURce:FREQuency:CW?")
        try:
            output = float(bla)
        except:
            print("Error in get_freq(): value returned: {0}".format(bla))
            output = -1.0
        return output

    def set_power(self, power_dBm):
        if (power_dBm >= -130) & (power_dBm <= 15):
            self.write(":SOURce:POWer {0}DBM".format(power_dBm))
        else:
            print("Error: power must be between -130 and 15 dBm")

    def get_power(self):
        bla = self.query(":SOURce:POWer?")
        try:
            output = float(bla)
        except:
            print("Error in get_power(): value returned: {0}".format(bla))
            output = -1.0
        return output

class EXG(MXG):

    def set_power(self, power_dBm):
        if (power_dBm >= -20) & (power_dBm <= 19):
            self.write(":SOURce:POWer {0}DBM".format(power_dBm))
        else:
            print("Error: power must be between -20 and 19 dBm")
