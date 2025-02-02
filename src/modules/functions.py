## *************************************** ##
        ## Function Repository file ##
## *************************************** ##
## ** Created by Gabriel Pizzighini and ... ** ## 

import os
import colorama as cl
import platform
import logging
import threading
import time
import board
import adafruit_bme680
import smbus
from .classes import *

# prints error [local]
def print_r(str):
    print(cl.Back.RED + str)

# prints in yellow [local]
def print_y(str):
    print(cl.Fore.YELLOW + str)

# print for the chamber simulator
def print_chamber(sensors_names,values,actuators_names,act_values):
    print(cl.Style.BRIGHT + "     ----------------------------- CHAMBER ------------------------------")
    print(f"                              "+cl.Style.BRIGHT + cl.Fore.BLACK +cl.Back.YELLOW + f"Time : {values[0]}",end='')
    print("                               ")
    if act_values[0] == 1:
        print(cl.Fore.YELLOW + f"                 {sensors_names[0]} : {values[1]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[0]} : " +cl.Back.GREEN + "ON")
    elif act_values[0] == 0:
        print(cl.Fore.YELLOW + f"                 {sensors_names[0]} : {values[1]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[0]} : " +cl.Back.RED + "OFF")
    if act_values[1] == 1:
        print(cl.Fore.LIGHTBLUE_EX  + f"                    {sensors_names[1]} : {values[2]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[1]} : " +cl.Back.GREEN + "ON")
    elif act_values[1] == 0:
        print(cl.Fore.LIGHTBLUE_EX  + f"                    {sensors_names[1]} : {values[2]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[1]} : " +cl.Back.RED + "OFF")
    if act_values[2] == 1:
        print(cl.Fore.MAGENTA + f"                         {sensors_names[2]} : {values[3]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[2]} : " +cl.Back.GREEN + "ON")
    elif act_values[2] == 0:
        print(cl.Fore.MAGENTA + f"                         {sensors_names[2]} : {values[3]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[2]} : " +cl.Back.RED + "OFF")
    if act_values[3] == 1:
        print(cl.Fore.CYAN + f"                          {sensors_names[3]} : {values[4]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[2]} : " +cl.Back.GREEN + "ON")
    elif act_values[3] == 0:
        print(cl.Fore.CYAN + f"                          {sensors_names[3]} : {values[4]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[2]} : " +cl.Back.RED + "OFF")
    if act_values[4] == 1:
        print(cl.Fore.RED + f"                    {sensors_names[4]} : {values[5]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[3]} : " +cl.Back.GREEN + "ON")
    elif act_values[4] == 0:
        print(cl.Fore.RED + f"                    {sensors_names[4]} : {values[5]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[3]} : " +cl.Back.RED + "OFF")
    print(cl.Style.BRIGHT + "     ------------------------- CTRL + C TO EXIT -------------------------")
    print(cl.Style.RESET_ALL)

# create simulated sensors
def create_sensors(names):
    Temperature_sensor = Sensor(name=names[0],min=12,max=24)
    Humidity_sensor = Sensor(name=names[1],min=10,max=80)
    CO2_sensor = Sensor(name=names[2],min=20,max=30)
    O2_sensor = Sensor(name=names[3],min=0.5,max=1)
    Pressure_sensor =  Sensor(name=names[4],min=10,max=20)

    # if needed add more sensors HERE:

    return Temperature_sensor, Humidity_sensor, CO2_sensor , O2_sensor, Pressure_sensor

def start_simulation(names,size):
    cl.init(autoreset=True)
    var = 0
    # Create sensors for the main loop
    Temp_sensor, Hum_sensor, CO2_sensor , O2_sensor, Press_sensor = create_sensors(names)
    while (var < size):
        t = dt.datetime.now().strftime('%M:%S.%f')

        # generate gauss values
        Temp_sensor.generate_value()
        Hum_sensor.generate_value()
        CO2_sensor.generate_value()
        O2_sensor.generate_value()
        Press_sensor.generate_value()

        # If you want to change any sensor value use the "set_value" class function
        # Be aware this needs to be done AFTER the generate values function
        # Uncomment the example bellow to change the value of the temperature sensor to 16
        # ********
        # Temp_sensor.set_value(16)
        # ********

        # get the generated values
        temp = Temp_sensor.get_value()
        hum = Hum_sensor.get_value()
        co2 = CO2_sensor.get_value()
        o2 = O2_sensor.get_value()
        press = Press_sensor.get_value()

        # print values on terminal 
        print(cl.Style.BRIGHT + f"----------------------------- START SENSORS READINGS ({var}/{size}) ------------------------------")
        print(cl.Style.BRIGHT + cl.Back.YELLOW + cl.Fore.WHITE + f"Time : {t} ")
        print(cl.Fore.YELLOW + f"{names[0]} : {temp}")
        print(cl.Fore.BLUE + f"{names[1]} : {hum}")
        print(cl.Fore.MAGENTA + f"{names[2]} : {co2}")
        print(cl.Fore.CYAN + f"{names[3]} : {o2}")
        print(cl.Fore.RED + f"{names[4]} : {press}")
        print(cl.Style.BRIGHT + f"----------------------------- CTRL + C TO EXIT ------------------------------------")
        print(cl.Style.RESET_ALL)

        time.sleep(1)
        var += 1

# simulate the values for the sensors [local thread]
def simulate_function(name):
    logging.info("Thread %s: starting", name)
    # Create the sensors names
    sensors_names = ["Temp", "Hum", "CO2", "O2", "Pressure"]
    print(cl.Fore.YELLOW + "How many values to simulate? size = ",end='')
    ans = int(input())
    start_simulation(sensors_names,ans)

    logging.info("Thread %s: finishing", name)

#initializes the system [main.py] --> shows the ASCII art and identifies the execution environment  
def initialize_system():
    cl.init(autoreset=True)
    try: 
        # ASCII art
        f = open('../rep/header.txt', 'r')
        print(f.read())
        f.close()
    except:
        print_r("ERROR-[1] : Failed opening ASCII art")
    
    try:
        if platform.uname()[4].startswith("aarch64"):
            print(cl.Back.GREEN + f"Executing on {platform.uname()[4]}")
            return 1
        else:
            print_r("ERROR-[2] : Didn't found an ARM chip 'BCM***' module, please execute me in Raspberry Pi or similar...")
            print(cl.Back.RED + f"You are on a {platform.system()} system")
            return 2
    except:
            print_r("ERROR-[3] : Unable to obtain the base model of the device")

# Start the execution of the simulation file [main.py]  
def initialize_simulator():
    try:
        sim = threading.Thread(target=simulate_function, args=(1,))
        sim.start()
    except:
        print_r("ERROR-[4] : Unable to start the simulator")

def initialize_real_sensors():
    """
    Check if all sensors are connected
    @param\n
    Location - defines the geographical location of the raspberry, supported locations = [PT] & [BR]
    """
    bus = smbus.SMBus(1)
    i2c = board.I2C()  # uses board.SCL and board.SDA

    try:
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
        print("[" + cl.Fore.GREEN + "OK" + cl.Fore.WHITE + "]" + "- BME680 connected")

    except:
        print("[" + cl.Fore.RED + "NOT FOUND" + cl.Fore.WHITE + "]" + "- BME680 not found") 
        pass

def read_real_sensors(Location: str):
    """
    Read data from the sensors\n
    @param\n
    Location - defines the geographical location of the raspberry, supported locations = [PT] & [BR]
    @return\n
    [1] - Temperature in celsius\n
    [2] - Gas\n
    [3] - Humidity\n
    [4] - Pressure in hPa\n
    """
    bus = smbus.SMBus(1)
    i2c = board.I2C()  # uses board.SCL and board.SDA
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

    try:
        # Calibration of pressure
        if Location == "PT":
            # change this to match the location's pressure (hPa) at sea level
            bme680.sea_level_pressure = 1008.5

        elif Location == "BR":
            # change this to match the location's pressure (hPa) at sea level
            bme680.sea_level_pressure = 1012.5
        else: 
            print_r(f"ERROR-[4] : Location '{Location}' not found or invalid")
        # temperature calibration
        temperature_offset = -5
        return bme680.temperature + temperature_offset, bme680.gas, bme680.relative_humidity, bme680.pressure
        
    except:
        print_r(f"ERROR-[5] : Unable to start real sensors ")

def start(argv)->int:
    '''
    Mode function to protect the database 
    '''
    try:
        if argv[1] == 'DEBUG':
            print("Entering" + cl.Fore.LIGHTYELLOW_EX + " DEBUG " + cl.Fore.WHITE + "mode to protect from database flood")
            return 0

        elif argv[1] == 'NORMAL':
            print("Entering" + cl.Fore.LIGHTGREEN_EX + " NORMAL " + cl.Fore.WHITE + "mode")
            return 1

        else:
            print("INVALID argument to main.py! please choose one of the following...")
            print("DEBUG - for debug process (this mode will protect the database from flooding)")
            print("NORMAL - for normal program execution")
            print("EXAMPLE - $ sudo python3 main.py DEBUG")
            return 2

    except:
            print("MISSING argument to main.py! please choose one of the following...")
            print("DEBUG - for debug process (this mode will protect the database from flooding)")
            print("NORMAL - for normal program execution")
            print("EXAMPLE - $ sudo python3 main.py DEBUG") 