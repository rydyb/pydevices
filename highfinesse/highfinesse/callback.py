######################################################################################################
# @file CallBackDemo.py
# @copyright HighFinesse GmbH.
# @author Lovas Szilard <lovas@highfinesse.de>
# @date 2018.09.16
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#
# @brief Python language example for demonstrating usage of wlmData.dll CallBack mechanism.
# Tested with Python 3.7.
# 64-bit Python requires 64-bit wlmData.dll (in System32 folder) and
# 32-bit Python requires 32-bit wlmData.dll (in SysWOW64 folder on Win64 or System32 folder on Win32).
# For more information see the ctypes module documentation:
# https://docs.python.org/3/library/ctypes.html
# and/or WLM manual.pdf
#
# Changelog:
# ----------
# 2018.09.16
# v0.1 - Initial release
#

import sys
import time

# wlmData.dll related imports
import wlmConst
import wlmData

# Set the data acquisition time (sec) here:
DATA_ACQUISITION_TIME = 5

# Set the callback thread priority here:
CALLBACK_THREAD_PRIORITY = 2


# Create callback function pointer
@wlmData.CALLBACK_TYPE
def my_callback(mode, _intval, dblval):
    """This wlmData callback function simply prints the received wavelength
    results"""

    if mode == wlmConst.cmiWavelength1:
        print(f"Ch1 wavelength (vac.): {dblval} nm")
    elif mode == wlmConst.cmiWavelength2:
        print(f"Ch2 wavelength (vac.): {dblval} nm")
    elif mode == wlmConst.cmiWavelength3:
        print(f"Ch3 wavelength (vac.): {dblval} nm")
    elif mode == wlmConst.cmiWavelength4:
        print(f"Ch4 wavelength (vac.): {dblval} nm")
    elif mode == wlmConst.cmiWavelength5:
        print(f"Ch5 wavelength (vac.): {dblval} nm")
    elif mode == wlmConst.cmiWavelength6:
        print(f"Ch6 wavelength (vac.): {dblval} nm")
    elif mode == wlmConst.cmiWavelength7:
        print(f"Ch7 wavelength (vac.): {dblval} nm")
    elif mode == wlmConst.cmiWavelength8:
        print(f"Ch8 wavelength (vac.): {dblval} nm")
    elif mode == wlmConst.cmiTemperature:
        print(f"Temperature: {dblval} C")
    elif mode == wlmConst.cmiPressure:
        print(f"Pressure: {dblval} mbar")


# Load wlmData library. If needed, adjust the path by passing it to LoadDLL()!
try:
    dll = wlmData.LoadDLL()
    # dll = wlmData.LoadDLL('/path/to/your/libwlmData.so')
except OSError as err:
    sys.exit(f"{err}\nPlease check if the wlmData DLL is installed correctly!")

# Check the number of WLM server instances
if dll.GetWLMCount(0) == 0:
    sys.exit("There is no running WLM server instance.")

print(f"Data acquisition by callback function for {DATA_ACQUISITION_TIME} seconds.")

# Install callback function
dll.Instantiate(
    wlmConst.cInstNotification,
    wlmConst.cNotifyInstallCallback,
    my_callback,
    CALLBACK_THREAD_PRIORITY,
)

# Give a little time for data acquisition
time.sleep(DATA_ACQUISITION_TIME)

# Remove callback function
dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, None, 0)

print("Callback function was removed.")
