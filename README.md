reflow_oven
===========
![Screenshot](screenshot.png)

This goal of this project is to create a reflow oven using a toaster oven.  The project consists of two components: an Arduino based temperature controller and a GUI written in Python.  The temperature controller is similar to a thermostat.  Commands are received via the serial port to set the desired temperature.  The temperature controller switches the heater ON if the temperature is less than the desired temperature.  Once the temperature exceeds the desired temperature the heater is turned OFF.  The GUI written in Python calculates the desired temperature at each second using the provided reflow parameters.  Next, the GUI steps through the calculated profile sending the desired temperature to the Arduino and graphing the actual temperature against the desired temperature.

