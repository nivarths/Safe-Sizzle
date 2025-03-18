import busio
import board
import smbus
import time
from math import pow

# Install Library files by typing "sudo pip3 install adafruit-circuitpython-amg88xx" at the Terminal.
class Temperature_Sensor(object):

    def __init__(self):
        import adafruit_amg88xx
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.amg = adafruit_amg88xx.AMG88XX(self.i2c)

    def temp_array(self): # 8x8 array of temperature values in degrees C
        return self.amg.pixels

    def temp_list(self): # 64-item list of temperature values in degrees C
        self.data_list = []
        for row in self.amg.pixels:
            for temp in row:
                self.data_list.append(temp)
        return self.data_list

    def avg_temp(self): # average temperature value of 8x8 array, in degrees C
        total = 0
        count = 0
        for row in self.amg.pixels:
            for temp in row:
                total += temp
                count += 1
        self.avg = total / count
        return self.avg

    def max_temp(self): # maximum temperature value of 8x8 array, in degrees C
        self.data_list = self.temp_list()
        return max(self.data_list)
        
    def min_temp(self): # minimum temperature value of 8x8 array, in degrees C
        self.data_list = self.temp_list()
        return min(self.data_list)




# Install Library files by typing "sudo pip3 install adafruit-circuitpython-vl53l0x" at the Terminal
class Distance_Sensor(object):

    def __init__(self):
        import adafruit_vl53l0x
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.vl53 = adafruit_vl53l0x.VL53L0X(self.i2c)

    def distance(self): # distance from bottom of sensor in millimetres (mm)
        return self.vl53.range

    def timing(self,value=33000): # adjusts the measurement timing budget to change speed and accuracy (optional)
        self.vl53.measurement_timing_budget = value
        """ The default timing budget is 33ms, a good compromise of speed and accuracy
            For example a higher speed but less accurate timing budget of 20ms: value = 20000
            Or a slower but more accurate timing budget of 200ms: value = 200000 """




#Install Library files by typing "sudo pip3 install adafruit-circuitpython-bno055" at the Terminal.
class Orientation_Sensor(object):

    def __init__(self):
        import adafruit_bno055
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.bno055 = adafruit_bno055.BNO055_I2C(self.i2c)
        #self.bno055 = adafruit_bno055.BNO055(self.i2c)

    def euler_angles(self): # 3-axis orientation in angular degrees 
        return self.bno055.euler

    def lin_acceleration(self): # 3-axis vector of linear acceleration in m/s^2 (acceleration - gravity)
        return self.bno055.linear_acceleration

    def accelerometer(self): # 3-axis vector of acceleration in m/s^2 (gravity + linear motion)
        return self.bno055.acceleration

    def gravity(self): # 3-axis vector of gravitational acceleration in m/s^2 (minus any movement)
        return self.bno055.gravity

    def gyroscope(self): # 3-axis vector of gyroscope values in radians per second
        return self.bno055.gyro

    def temperature(self): # ambient temperature in degrees C
        return self.bno055.temperature

    def magnetic_field(self): # magnetic field strength vector in micro-Tesla (uT)
        return self.bno055.magnetic




class Force_Sensing_Resistor(object):

    def __init__(self,pin=0,i2c_ch=1):
        self.address = 0x48
        self.A0 = 0x40
        self.A1 = 0x41
        self.A2 = 0x42
        self.A3 = 0x43
        self.pin = pin
        self.bus = smbus.SMBus(i2c_ch)

    def force_raw(self):
        if self.pin == 0:
            self.bus.write_byte(self.address,self.A0)
        elif self.pin == 1:
            address = 0x48
            A1 = 0x41
            self.bus.write_byte(self.address,self.A1)
        elif self.pin == 2:
            self.bus.write_byte(self.address,self.A2)
        elif self.pin == 3:
            self.bus.write_byte(self.address,self.A3)
        else:
            print("Incorrect value.  Pin defaulted to 0")
            self.bus.write_byte(self.address,self.A0)
        self.value = self.bus.read_byte(self.address)
        return self.value

    def force_scaled(self,scale=5):
        self.force_raw()
        self.scaled = self.force_raw() * scale / 255
        return self.scaled




class Muscle_Sensor(object):

    def __init__(self,pin=0,i2c_ch=1):
        self.address = 0x48
        self.A0 = 0x40
        self.A1 = 0x41
        self.A2 = 0x42
        self.A3 = 0x43
        self.pin = pin
        self.bus = smbus.SMBus(i2c_ch)

    def muscle_raw(self):
        if self.pin == 0:
            self.bus.write_byte(self.address,self.A0)
        elif self.pin == 1:
            address = 0x48
            A1 = 0x41
            self.bus.write_byte(self.address,self.A1)
        elif self.pin == 2:
            self.bus.write_byte(self.address,self.A2)
        elif self.pin == 3:
            self.bus.write_byte(self.address,self.A3)
        else:
            print("Incorrect value.  Pin defaulted to 0")
            self.bus.write_byte(self.address,self.A0)
        self.value = self.bus.read_byte(self.address)
        return self.value

    def muscle_scaled(self,scale=10):
        self.muscle_raw()
        self.scaled = self.muscle_raw() * scale / 255
        #self.force_raw()
        #self.scaled = self.force_raw() * scale / 255
        return self.scaled




class Heart_Rate_Sensor(object):

    def __init__(self):
        self.millis = lambda: int(round(time.time() * 1000))
        self.numberOfBeats = 5
        self.temp = [0]*(self.numberOfBeats+1)
        self.temp[-1] = self.millis()
        self.counter = 0
        self.sub = -1
        self.data_effect = True
        self.bpm_value = -1
        self.max_heartpulse_duty = 2000

    def sum_bpm(self):
        if self.data_effect:
            self.bpm_value = (60*self.numberOfBeats*1000)/(self.temp[self.numberOfBeats]-self.temp[0])
        self.data_effect = True

    def interrupt(self,null):
        self.temp[self.counter] = self.millis()
        if self.counter == 0:
            self.sub = self.temp[self.counter]-self.temp[self.numberOfBeats]
        else:
            self.sub = self.temp[self.counter]-self.temp[self.counter-1]
        if self.sub > self.max_heartpulse_duty:
            self.data_effect = False
            self.counter = 0
            print("BPM: ???")
            self.initialize_array()
            #self.arrayInit()
        if self.counter == self.numberOfBeats and self.data_effect:
            self.counter = 0
            self.sum_bpm()
        elif self.counter != self.numberOfBeats and self.data_effect:
            self.counter += 1
        else:
            self.counter = 0
            self.data_effect = True

    def initialize_array(self):
        self.temp = [0]*(self.numberOfBeats+1)
        self.temp[-1] = self.millis()

    def heart_rate(self):
        return int(self.bpm_value)


        

class Gas_Sensor(object):
    DEFAULT_I2C_ADDR = 0x04

    ADDR_IS_SET = 0  # if this is the first time to run, if 1126, set
    ADDR_FACTORY_ADC_NH3 = 2
    ADDR_FACTORY_ADC_CO = 4
    ADDR_FACTORY_ADC_NO2 = 6

    ADDR_USER_ADC_HN3 = 8
    ADDR_USER_ADC_CO = 10
    ADDR_USER_ADC_NO2 = 12
    ADDR_IF_CALI = 14  # IF USER HAD CALI

    ADDR_I2C_ADDRESS = 20

    CH_VALUE_NH3 = 1
    CH_VALUE_CO = 2
    CH_VALUE_NO2 = 3

    CMD_ADC_RES0 = 1  # NH3
    CMD_ADC_RES1 = 2  # CO
    CMD_ADC_RES2 = 3  # NO2
    CMD_ADC_RESALL = 4  # ALL CHANNEL
    CMD_CHANGE_I2C = 5  # CHANGE I2C
    CMD_READ_EEPROM = 6  # READ EEPROM VALUE, RETURN UNSIGNED INT
    CMD_SET_R0_ADC = 7  # SET R0 ADC VALUE
    CMD_GET_R0_ADC = 8  # GET R0 ADC VALUE
    CMD_GET_R0_ADC_FACTORY = 9  # GET FACTORY R0 ADC VALUE
    CMD_CONTROL_LED = 10
    CMD_CONTROL_PWR = 11

    CO = 0
    NO2 = 1
    NH3 = 2
    C3H8 = 3
    C4H10 = 4
    CH4 = 5
    H2 = 6
    C2H5OH = 7

    adcValueR0_NH3_Buf = 0
    adcValueR0_C0_Buf = 0
    adcValueR0_NO2_Buf = 0

    def __init__(self, addr=DEFAULT_I2C_ADDR):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.addr = addr
        self.version = self.get_version()

    def cmd(self, cmd, nbytes=2):
        self.i2c.writeto(self.addr, bytes(cmd))
        dta = 0
        buf = bytearray(nbytes)
        raw = self.i2c.readfrom_into(self.addr, buf)
        for byte in buf:
            dta = dta * 256 + int(byte)
        if cmd == self.CH_VALUE_NH3:
            if dta > 0:
                self.adcValueR0_NH3_Buf = dta
            else:
                dta = self.adcValueR0_NH3_Buf
        elif cmd == self.CH_VALUE_CO:
            if dta > 0:
                self.adcValueR0_CO_Buf = dta
            else:
                dta = self.adcValueR0_CO_Buf
        elif cmd == self.CH_VALUE_NO2:
            if dta > 0:
                self.adcValueR0_NO2_Buf = dta
            else:
                dta = self.adcValueR0_NO2_Buf
        return dta

    def get_version(self):
        if self.cmd([self.CMD_READ_EEPROM, self.ADDR_IS_SET]) == 1126:
            return 2
        else:
            print("version currently not supported")
            from sys import exit
            exit(1)

    def CO_gas(self): # Carbon Monoxide gas, in ppm (parts per million)
        A0_1 = self.cmd([6, self.ADDR_USER_ADC_CO])
        An_1 = self.cmd([self.CH_VALUE_CO])
        ratio1 = An_1 / A0_1 * (1023.0 - A0_1) / (1023.0 - An_1)
        c = pow(ratio1, -1.179) * 4.385
        return c

    def NO2_gas(self): # Nitrogen Dioxide gas, in ppm
        A0_2 = self.cmd([6, self.ADDR_USER_ADC_NO2])
        An_2 = self.cmd([self.CH_VALUE_NO2])
        ratio2 = An_2 / A0_2 * (1023.0 - A0_2) / (1023.0 - An_2)
        c = pow(ratio2, 1.007) / 6.855
        return c

    def H2_gas(self): # Hydrogen, in ppm
        A0_1 = self.cmd([6, self.ADDR_USER_ADC_CO])
        An_1 = self.cmd([self.CH_VALUE_CO])
        ratio1 = An_1 / A0_1 * (1023.0 - A0_1) / (1023.0 - An_1)
        c = pow(ratio1, -1.8) * 0.73
        return c

    def ammonia(self): # Ammonia (NH3), in ppm
        A0_0 = self.cmd([6, self.ADDR_USER_ADC_HN3])
        An_0 = self.cmd([self.CH_VALUE_NH3])
        ratio0 = An_0 / A0_0 * (1023.0 - A0_0) / (1023.0 - An_0)
        c = pow(ratio0, -1.67) / 1.47
        return c

    def propane(self): # Propane (C3H8), in ppm
        A0_0 = self.cmd([6, self.ADDR_USER_ADC_HN3])
        An_0 = self.cmd([self.CH_VALUE_NH3])
        ratio0 = An_0 / A0_0 * (1023.0 - A0_0) / (1023.0 - An_0)
        c = pow(ratio0, -2.518) * 570.164
        return c

    def butane(self): # Butane (C4H10), in ppm
        A0_0 = self.cmd([6, self.ADDR_USER_ADC_HN3])
        An_0 = self.cmd([self.CH_VALUE_NH3])
        ratio0 = An_0 / A0_0 * (1023.0 - A0_0) / (1023.0 - An_0)
        c = pow(ratio0, -2.138) * 398.107
        return c

    def methane(self): # Methane (CH4), in ppm
        A0_1 = self.cmd([6, self.ADDR_USER_ADC_CO])
        An_1 = self.cmd([self.CH_VALUE_CO])
        ratio1 = An_1 / A0_1 * (1023.0 - A0_1) / (1023.0 - An_1)
        c = pow(ratio1, -4.363) * 630.957
        return c

    def ethanol(self): # Ethanol (C2H5OH), in ppm
        A0_1 = self.cmd([6, self.ADDR_USER_ADC_CO])
        An_1 = self.cmd([self.CH_VALUE_CO])
        ratio1 = An_1 / A0_1 * (1023.0 - A0_1) / (1023.0 - An_1)
        c = pow(ratio1, -1.552) * 1.622
        return c
        

