import pyftdi.gpio as gpio

class USBs:
    """ This class handles all USB functionality"""
    def __init__(self):
        __gpioController = gpio.GpioController

    def modifyBit(byte: int, targetBit: int, on: bool) -> int:
        """ Modify the target bit's value to either on or off in the given byte. Does not modify the other bits"""
        if on:
            return byte | (1 << targetBit)
        else:
            return byte & (~ (
                    0x01 << targetBit))  # set the target bit to 1 and then invert the bits so target is a 0 and all others are Ones. Then and with the given byte

