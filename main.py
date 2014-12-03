#TODO: Implement serial port selector
#TODO: Integrate temperature controller

from Tkinter import *
from threading import *
from random import *
from profile_widget import ProfileWidget
from reflow import Reflow
from temperature_controller import TemperatureController
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import os
import re
import time
import uuid
import json

#--------------------------------------------------------------------------------
# !!! SIG AND LICENSE GO HERE !!!
#--------------------------------------------------------------------------------
signature = [127, 194, 96, 226, 7, 22, 71, 171, 55, 160, 173, 212, 113, 93, 57, 152, 88, 119, 133, 90, 84, 181, 223, 133, 86, 170, 127, 138, 160, 93, 101, 25, 243, 16, 174, 123, 231, 103, 137, 34, 115, 165, 55, 38, 236, 188, 180, 60, 151, 54, 119, 209, 40, 171, 2, 43, 147, 120, 61, 237, 237, 159, 105, 9, 167, 47, 200, 161, 61, 105, 108, 138, 215, 212, 244, 88, 40, 135, 40, 126, 9, 196, 173, 34, 25, 224, 194, 239, 100, 168, 184, 210, 247, 43, 32, 140, 181, 145, 157, 68, 248, 90, 129, 99, 81, 206, 5, 212, 193, 45, 110, 208, 79, 242, 193, 155, 133, 61, 226, 93, 76, 187, 22, 133, 236, 131, 45, 164, 217, 85, 176, 168, 230, 25, 251, 221, 3, 219, 195, 110, 61, 192, 93, 234, 34, 32, 203, 199, 7, 221, 182, 21, 156, 18, 103, 72, 186, 196, 84, 35, 149, 80, 16, 191, 47, 54, 224, 100, 231, 46, 89, 0, 179, 168, 25, 66, 142, 41, 196, 234, 198, 248, 250, 17, 70, 244, 234, 239, 64, 57, 115, 234, 83, 101, 125, 103, 167, 91, 104, 194, 17, 203, 181, 11, 191, 202, 234, 56, 51, 51, 198, 55, 168, 162, 110, 89, 175, 140, 125, 205, 177, 149, 20, 253, 124, 210, 128, 77, 239, 157, 214, 16, 143, 241, 76, 253, 209, 43, 127, 164, 68, 208, 141, 29, 172, 213, 93, 205, 224, 228, 240, 187, 220, 106, 115, 251, ]
license = '{"expiration":1449031259,"id":"08f9e385-2ae3-4678-a12d-9f91de9e95c0","name":"Kris Barrett","nodes":[66002175764577,121375392182],"product":"Reflow Oven Controller"}'
#--------------------------------------------------------------------------------

# Key
pubkey = "-----BEGIN PUBLIC KEY-----\n\
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwmD1/b94/nJqc8J03pWh\n\
UrAUlAJtPyCvEyQEtrIJPmXRB0Uhhm29rVgkzD4zCdWl/HU9dPO0e7YKLz2VrTeR\n\
Uy1TvvyMRsAaQWbFlNhxYO1aEGKOumM1S3yB+AxzhSugTy791YJ+drhSTDCkYHg8\n\
CyU/4Tm2YBBVF7nReBqpEnu6/TFIpMDX0dv0xEtr5TyYYhYOfMksYyQ11Wy2hFlz\n\
34BlhEFPIW7LxOgoUEqeRtG9Ci9gWiy09EuR4bumE7UTCXu2zUJchtazkt+cEO0o\n\
a3SWzTgpv4gBYyR26rqg8EtSr0GQTKV6sOLGMUgsmsBEOo1Dr4qK3w0UXW7dPBiC\n\
9wIDAQAB\n\
-----END PUBLIC KEY-----"

# Signature
sig = ""
for i in signature:
	sig += chr(i)

# Verify License
key = RSA.importKey(pubkey)
h = SHA.new(license)
verifier = PKCS1_v1_5.new(key)
if not verifier.verify(h, sig):
	print "Invalid license"
	sys.exit(1)

# Check node
license = json.loads(license)
node = uuid.getnode()
try:
	license['nodes'].index(node)
except:
	print('You are not authorized to use this software on this machine')
	print('Licensed for ' + license['name'])
	print(node)
	sys.exit(1)

# Check expiration
current_time = int(time.time())
if current_time > license['expiration']:
	print('License is expired')
	sys.exit(1)

# Get serial ports
serial_ports = []
if sys.platform == 'darwin':
	files = os.listdir("/dev")
	serial_ports.append("-")
	for f in files:
		match = re.search("tty[\.U]", f)
		if match != None:
			serial_ports.append("/dev/" + f)

def update():
	global i, update_timer, temp_controller
	actual  = temp_controller.set_temp(profile.desired[i])
	if(i > 0):
		expected = profile.desired[i-1]
		error = 100 * (actual - expected) / expected
		print '%(i)d,%(actual).2f,%(expected).2f,%(error).2f' % \
			{"i": i, "actual": actual, "expected": expected, "error": error} 
		profile.add_actual(actual)
	i = i + 1
	if i < len(profile.desired):
		update_timer = Timer(1, update)
		update_timer.start()
	
def start_button_clicked():
	global i, update_timer, temp_controller
	print "start clicked"
	if serial_var.get() == "-":
		return
	temp_controller = TemperatureController(serial_var.get())
	# wait for arduino to reboot
	time.sleep(3)
	temp_controller.set_temp(starting_var.get())
	# while(temp_controller.temp() <= starting_var.get()):
	# 	time.sleep(1)
	desired = Reflow.reflow(starting_temp=temp_controller.temp(),  
		preheat_min=float(preheat_min_var.get()), 
		preheat_max=float(preheat_max_var.get()), 
		peak_temp=float(peak_temp_var.get()), 
		flow_temp=float(flow_temp_var.get()), 
		ramp_up=float(ramp_up_var.get()), 
		ramp_down=float(ramp_down_var.get()), 
		preheat_time=float(preheat_time_var.get()), 
		peak_time=float(peak_time_var.get()), 
		flow_time=float(flow_time_var.get()))
	profile.desired = desired
	profile.redraw()
	if update_timer != None:
		update_timer.cancel()
	i = 0
	update()
	
def preview_button_clicked():
	print "preview clicked"
	desired = Reflow.reflow(50,  
		preheat_min=float(preheat_min_var.get()), 
		preheat_max=float(preheat_max_var.get()), 
		peak_temp=float(peak_temp_var.get()), 
		flow_temp=float(flow_temp_var.get()), 
		ramp_up=float(ramp_up_var.get()), 
		ramp_down=float(ramp_down_var.get()), 
		preheat_time=float(preheat_time_var.get()), 
		peak_time=float(peak_time_var.get()), 
		flow_time=float(flow_time_var.get()))
	profile.desired = desired
	profile.redraw()

# root
root = Tk()
root.wm_title("Reflow Controller")

# profile widget
width = 640
height = 480
profile = ProfileWidget(width, height)
profile.canvas.grid(row=0, column=0, padx=10, pady=10)
Label(root, text="Reflow Controller").grid(row=0, column=1)

# frame
frame = Frame(root)
frame.grid(row=0, column=1)

# serial_listbox
serial_label = Label(frame, text="Serial Port: ")
if sys.platform == 'darwin':
	serial_var = StringVar(root)
	serial_var.set(serial_ports[0])
	serial_option = apply(OptionMenu, (frame, serial_var) + tuple(serial_ports))
	serial_label.grid(row=1, column=0)
	serial_option.grid(row=1, column=1)
elif sys.platform == 'win32':
	serial_var = StringVar(root)
	serial_entry = Entry(frame, textvariable=serial_var)
	serial_entry.insert(0,"COM1")
	serial_label.grid(row=1, column=0)
	serial_entry.grid(row=1, column=1)


# ramp up
degrees_c = unichr(176) + "C"
ramp_up_label = Label(frame, text="Ramp Up (" + degrees_c + "/s): ")
ramp_up_var = StringVar(root)
ramp_up_entry = Entry(frame, textvariable=ramp_up_var)
ramp_up_entry.insert(0,1.5)
ramp_up_label.grid(row=2, column=0)
ramp_up_entry.grid(row=2, column=1)

# ramp down
ramp_down_label = Label(frame, text="Ramp Down (" + degrees_c + "/s): ")
ramp_down_var = StringVar(root)
ramp_down_entry = Entry(frame, textvariable=ramp_down_var)
ramp_down_entry.insert(0,2)
ramp_down_label.grid(row=3, column=0)
ramp_down_entry.grid(row=3, column=1)

# preheat min
starting_label = Label(frame, text="Starting (" + degrees_c + "): ")
starting_var = StringVar(root)
starting_entry = Entry(frame, textvariable=starting_var)
starting_entry.insert(0,50)
starting_label.grid(row=4, column=0)
starting_entry.grid(row=4, column=1)

# preheat min
preheat_min_label = Label(frame, text="Preheat Min (" + degrees_c + "): ")
preheat_min_var = StringVar(root)
preheat_min_entry = Entry(frame, textvariable=preheat_min_var)
preheat_min_entry.insert(0,140)
preheat_min_label.grid(row=5, column=0)
preheat_min_entry.grid(row=5, column=1)

# preheat max
preheat_max_label = Label(frame, text="Preheat Max (" + degrees_c + "): ")
preheat_max_var = StringVar(root)
preheat_max_entry = Entry(frame, textvariable=preheat_max_var)
preheat_max_entry.insert(0,200)
preheat_max_label.grid(row=6, column=0)
preheat_max_entry.grid(row=6, column=1)

# preheat time
preheat_time_label = Label(frame, text="Preheat Time (s): ")
preheat_time_var = StringVar(root)
preheat_time_entry = Entry(frame, textvariable=preheat_time_var)
preheat_time_entry.insert(0,90)
preheat_time_label.grid(row=7, column=0)
preheat_time_entry.grid(row=7, column=1)

# flow temp
flow_temp_label = Label(frame, text="Flow Temp (" + degrees_c + "): ")
flow_temp_var = StringVar(root)
flow_temp_entry = Entry(frame, textvariable=flow_temp_var)
flow_temp_entry.insert(0,219)
flow_temp_label.grid(row=8, column=0)
flow_temp_entry.grid(row=8, column=1)

# flow time
flow_time_label = Label(frame, text="Flow Time (s): ")
flow_time_var = StringVar(root)
flow_time_entry = Entry(frame, textvariable=flow_time_var)
flow_time_entry.insert(0,60)
flow_time_label.grid(row=9, column=0)
flow_time_entry.grid(row=9, column=1)

# peak temp
peak_temp_label = Label(frame, text="Peak Temp (" + degrees_c + "): ")
peak_temp_var = StringVar(root)
peak_temp_entry = Entry(frame, textvariable=peak_temp_var)
peak_temp_entry.insert(0,250)
peak_temp_label.grid(row=10, column=0)
peak_temp_entry.grid(row=10, column=1)

# peak time
peak_time_label = Label(frame, text="Peak Time (s): ")
peak_time_var = StringVar(root)
peak_time_entry = Entry(frame, textvariable=peak_time_var)
peak_time_entry.insert(0,10)
peak_time_label.grid(row=11, column=0)
peak_time_entry.grid(row=11, column=1)

# preview button
preview_button = Button(frame, text="Preview", command=preview_button_clicked)
preview_button.grid(row=12, column=1)

# start button
start_button = Button(frame, text="Start", command=start_button_clicked)
start_button.grid(row=13, column=1)

# update_timer
update_timer = None

# run
root.mainloop()
