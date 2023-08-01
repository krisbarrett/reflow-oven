import serial

class TemperatureController:
	def __init__(self, serial_port):
		self.serial = serial.Serial(serial_port, timeout=1)

	def cmd(self, cmd, arg=""):
		stuff = cmd + " " + str(arg) + chr(10)
		self.serial.write(stuff)
		result = self.serial.readline()
		if(result == ""):
			return 0
		else:
			return result

	def set_temp(self, temp):
		return float(self.cmd("set_temp", temp))

	def temp(self):
		return float(self.cmd("temp"))

	def hyst_high(self, temp):
		response = self.cmd("hyst_high", temp)
		if response == "err":
			print("An error occurred while setting hyst_high")

	def hyst_low(self, temp):
		response = self.cmd("hyst_low", temp)
		if response == "err":
			print("An error occurred while setting hyst_low")
	
	def start(self):
		self.cmd("start")