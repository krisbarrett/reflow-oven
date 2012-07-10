import serial

class TemperatureController:
	def __init__(self, serial_port):
		self.serial = serial.Serial(serial_port)

	def cmd(self, cmd, arg=""):
		self.serial.write(cmd + arg + "\n")
		return self.readline()

	def set_temp(self, temp):
		return float(self.cmd("set_temp", temp))

	def temp(self):
		return float(self.cmd("temp"))

	def hyst_high(self, temp):
		response = cmd("hyst_high", temp)
		if response == "err":
			print "An error occurred while setting hyst_high"

	def hyst_low(self, temp):
		response = cmd("hyst_low", temp)
		if response == "err":
			print "An error occurred while setting hyst_low"