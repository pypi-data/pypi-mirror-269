from LEDAutomation.FtdiInterface import ExpanderGPIOAddress as addr
from LEDAutomation.FtdiInterface import GPIOEnum
## List out the pin addresses for the LED Buttons.

# Maybe have generic console class that takes in the map of buttons to GPIO pins and then has generic methods like clickButton(). FTDI interface would then parse the GPIO Mapping and determine where to send the command

# map of buttons to GPIO numbers. Console specific mapping? Maybe use an enum from the FTDIInterface as the value so it can be read easier?

# list out the GPIO expander Mapping in this class, which can then be used in the test scripts
class GPIOMap(GPIOEnum):
    #     #GPIO Expander, bank, pin
    PLAY = addr(0,0,0)
    PAUSE = addr(1,1,2)

