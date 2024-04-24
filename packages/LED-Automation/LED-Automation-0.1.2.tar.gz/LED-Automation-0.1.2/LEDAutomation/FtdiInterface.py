import pyftdi.i2c as i2c
from enum import IntFlag
from typing import List
from PCA9506 import GPIOEnum
from PCA9506 import ExpanderGPIOAddress
import PCA9506 as GPIOExpander
# Requires PyFTDI to be installed on the device and the FTDI device to be plugged in

# Scripts in the Scripts folder for finding connected i2C devices
# py .venv/Scripts/i2cscan.py


# Board won't be changing, so having items for the , pinout might change for the console buttons etc, so make sure those are provided via a map or something.
# goal is just to toggle buttons


# General Notes on code:
# a 1 bit is considered HIGH/UP/ACTIVE and a 0 bit is considered LOW/DOWN/INACTIVE in relation to documentation and schematics
# Register addresses are found in the documentation for the device that is controlling the LED's: in our case the PCA9506 chip
# Which pins on the chip that need to be used to toggle the LED's is located on the schematic for the board. This also shows which IO bank on the chip has the LED pins (IO_4 aka bank 4)

#General Flow:

# init the device
# toggle the pins you want to write to to output mode, this uses the config register for the pins.
# write to the output register for the pins. Each write will update the pins and update the device automatically
     
# use this to interact with I2C devices
class myFTDI:
    def __init__(self, address = "ftdi://::1/", interface:int = 1):

        # Interface 1 is I2C to the GPIO Expanders
        if(interface == 1):
            # init PyFTDI I2C controller for the specified interface aka group of 8 pins on the FTDI chip
            self.__i2cController = i2c.I2cController()
            self.__i2cController.configure(address + str(interface))
            #Init devices connected to I2C line
            self.PCA9506_A = GPIOExpander.PCA9506(self.__i2cController.get_port(0x22)) # I2C Address 0x22
            self.PCA9506_B = GPIOExpander.PCA9506(self.__i2cController.get_port(0x24)) # I2C Address 0x24? TODO need to verify
        
        # Interface 2 is SPI and connects to J107. Use the SPI communication protocol of PyFTDI to interact
        elif(interface == 2):
            self.newVar = False
            assert True
        
        # Interface 3 contains the pins for the USB hub I2c in a non standard pinout. This means we use the pyftdi.gpio library and manually implement the I2C protocol using it.
        elif(interface == 3):
            assert True
        
        # Interface 4 is manual and has the pins that control the thumbdrives. use the pyftdi.gpio library to manually interact with the pins.
        elif( interface == 4):
            assert True
        
        else:
            assert False, "Interface number was not a valid interface value; Valid 1-4 Yours: " + str(interface)


class Driver:
    """ Driver class that will be used in the Test classes"""
    
    class LEDS(GPIOEnum): # LED's addresses on the board can be hardcoded
        ONE = ExpanderGPIOAddress(0,4, 1)
        TWO = ExpanderGPIOAddress(0,4, 2)
        THREE = ExpanderGPIOAddress(0,4, 3)
        FOUR = ExpanderGPIOAddress(0,4, 4)

    def __init__(self, gpioConfigList: List[ExpanderGPIOAddress] ):
        """ Pass in the list of items on the GPIO to setup their config"""
        self.__GPIOMap = gpioConfigList
        self.__myFTDI = myFTDI(interface = 1)
        self.__setDefaultConfig(gpioConfigList) # Set the default GPIO Expander config

    def __verifyMapping(self, enumItem):
        """Safety check to make sure the passed in buttons implement the correct addresses and classes."""
        if not isinstance(enumItem, GPIOEnum):
            raise TypeError("Must pass in a GPIO Enum")
        if not isinstance(enumItem.value, ExpanderGPIOAddress):
            raise TypeError("Must assign addresses to your buttons")

    def __setDefaultConfig(self, gpiomapping:List[ExpanderGPIOAddress]):
        """ Set the mapped pins to be either input or output"""
        for led in self.LEDS.toList():
            targetExpander = self.__selectExpander(led.expander)
            targetExpander.writeToConfigPin(led, led.output)

        for button in gpiomapping:
            targetExpander = self.__selectExpander(button.expander)
            targetExpander.writeToConfigPin(button, button.output)

    def __selectExpander(self, expander:int):
        """Given the expander number, return the connection"""
        if(expander == 0):
            return self.__myFTDI.PCA9506_A
        else:
            return self.__myFTDI.PCA9506_B

    def toggleLED(self, led, on:bool):
        """ Toggle a given LED on or off """

        self.__verifyMapping(led)
        targetExpander = self.__selectExpander(led.value.expander)
        targetExpander.writeToOutputPin(led.value,on)
        
    def toggleButton(self, button, on:bool):
        """ Toggle a given button either on or off"""
        self.__verifyMapping(button)
        targetExpander = self.__selectExpander(button.value.expander)
        targetExpander.writeToOutputPin(button.value,on)

