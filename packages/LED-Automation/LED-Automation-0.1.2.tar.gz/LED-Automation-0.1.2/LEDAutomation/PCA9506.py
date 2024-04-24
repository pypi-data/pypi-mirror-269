import pyftdi.i2c as i2c
from enum import IntFlag
from typing import List
from enum import Enum

"""File containing all necessary code related to the GPIO Expanders model no PCA9506"""
    
   
class ExpanderGPIOAddress:
    """ This class stores the address for a pin: the GPIO expander it is on, the bank number, and the pin number. Also stores whether it should be input or output"""
    expander = None
    bank = None
    pin = None
    ouput = False
    def __init__(self, expander:int, bank:int, pin:int, output:bool = True):
        """ A class to store information important for things connected to the GPIO Expanders
            Args:
                expander(int): Expander that this relates to -> 0 or 1
                bank(int): Which bank the pin is on -> 0 through and including 4
                pin(int): The pin number in the bank -> 0 through and including 7
                output(bool): whether the pin should be output/write to or input/read from mode
        """
        self.__validateExpander(expander)
        self.__validateBank(bank)
        self.__validatePin(pin)
        self.expander = expander
        self.bank = bank
        self.pin = pin
        self.output = output
    def __validateExpander(self,expander):
        """ Make sure the expander number is either 0 or 1 """
        assert expander == 0 or expander == 1
    def __validateBank(self, bank):
        """ Make sure the bank number is valid and within range (0 - 4)"""
        assert bank >= 0 and bank <= 4
    def __validatePin(self, pin):
        """ Make sure the bit is within a byte aka """
        assert pin >= 0 and pin <= 7


class GPIOEnum(Enum):
    """Extend this enum in the Console specific GPIO Map file. Enforces type and gives a method to list out enum items"""
    @classmethod
    def toList(myEnum) -> List[ExpanderGPIOAddress]:
        """Convert the enum to a list of values"""
        return list(map(lambda c: c.value, myEnum))    
    

# Enum of registers that are available to write to
class PCAREG(IntFlag):
    IREG = 0x00 # Input Register
    OREG = 0x08 # Output Register
    PINT = 0x10 # Perform Interrupt Register
    IOCONFIG = 0x18 # IO Configuration Register
    MINT = 0x20 # Mask Interrupt Register

# Init this with I2C since that is where they connect
# Class that controls all the interactions with GPIO Expanders
class PCA9506:
    """This class controlls all the interactions with the GPIO Expanders. """
    __connection = None # The port that gets opened by the i2c controller. Use this to call the normal FTDI methods

    def __init__(self, i2CConnection: i2c.I2cPort):
        # store the connection so it can be used for other methods in the class
        self.__connection = i2CConnection

    # Core functions

    def __isValidBank(self,bank):
        """ Checks that the given bank number is valid, there are 5 banks labelled 0 through and including 4 """
        assert bank >= 0 and bank <=4

    def __writeToReg(self, address, bits:int):
        """Uses the pyftid write_to method
        Writes the bits to the specified address.

        Args:
            address (int): Hex address of the register to write to
            bits (int): The bits that we are writing
        """
        self.__connection.write_to(address, bits.to_bytes())
    
    def __readReg(self, address):
        """Reads the current bits of the target register"""
        return int.from_bytes(self.__connection.read_from(address, 1))

    def __readConfig(self, bank:int):
        """Read the byte stored in the given config bank"""
        self.__isValidBank(bank)
        return self.__readReg(bank | PCAREG.IOCONFIG)

    def __readPreviousOutput(self, bank: int):
        """Read in the previous byte that was output to the bank"""
        # TODO Optimize reading in previous state, to prevent having to directly read it in from the board every time?. Maybe cache the previous state when it is written or smth
        self.__isValidBank(bank)
        return self.__readReg(bank | PCAREG.OREG)

    def __readConfig(self, bank: int):
        # TODO Optimize reading in previous state, to prevent having to directly read it in from the board every time?. Maybe cache the previous state when it is written or smth
        self.__isValidBank(bank)
        return self.__readReg(bank | PCAREG.IOCONFIG)

    def __writeToConfig(self, bank:int, bits):
        """ Write to the config register for a bank of bits

        Args:
            bank (int): which bank to write to
            bits (bytearray): what values the bits aka pins should take
        """
        self.__isValidBank(bank)
        self.__writeToReg(bank | PCAREG.IOCONFIG, bits)

    def __writeToOutput(self, bank:int, bits):
        """ Write to the output for a bank
        Assumes that output is enabled already
        Args:
            bank (int): which bank to write to
            bits (bytearray): what values the bits aka pins should take
        """
        self.__isValidBank(bank)
        self.__writeToReg(bank | PCAREG.OREG, bits)
    
    def __modifyBit(self, byte:int, targetBit: int, on:bool):
        """ Modify the target bit's value to either on or off in the given byte. Does not modify the other bits"""
        if(on):
            return byte | (1 << targetBit)
        else:
            return byte & (~ (0x01 << targetBit) )  # set the target bit to 1 and then invert the bits so target is a 0 and all others are Ones. Then and with the given byte

    # Driver facing functions
        
    def writeToOutputPin(self, location:ExpanderGPIOAddress, value:bool):
        """ Write a value (True == 1, False == 0) to the given output pin """

        #print("Write to Output")
        # TODO Optimize reading in previous state, to prevent having to directly read it in from the board every time. Maybe cache the previous state when it is written/read or smth
        oldState = self.__readPreviousOutput(location.bank)
        #print("Old Pin State",bin(oldState))
        newState = self.__modifyBit(oldState,location.pin, value)
        #print("New Pin State",bin(newState))
        self.__writeToOutput(location.bank, newState )

    def writeToConfigPin(self, location:ExpanderGPIOAddress, setIsOutput:bool):
        """ Set a given pin to be output or input"""
        #print("Write Config")
        # TODO Optimize reading in previous state to prevent having to directly read it in from the board every time. Maybe cache the previous state when it is written/read or smth
        config = self.__readConfig(location.bank)
        #print(bin(config))
        newConf = self.__modifyBit(config,location.pin, not setIsOutput)
        #print(bin(newConf))
        self.__writeToConfig(location.bank, newConf) # 0 is output
