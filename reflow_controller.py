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
from Crypto.Cipher import AES
import os
import re
import time
import uuid
import json
import httplib
import urllib
from datetime import datetime

class ReflowController:
	def __init__(self):
		check1 = ''
		check2 = ''
		check3 = ''
		check4 = ''

		#--------------------------------------------------------------------------------
		# encrypted_payload and encrypted_public_key
		#--------------------------------------------------------------------------------
		encryption_key = [127, 194, 34, 166, 139, 10, 252, 13, 12, 33, 62, 156, 32, 156, 23, 161]
		encrypted_public_key = [82, 188, 242, 235, 51, 22, 165, 172, 8, 168, 51, 229, 227, 200, 40, 36, 122, 227, 206, 253, 210, 95, 103, 215, 204, 226, 127, 229, 143, 46, 88, 52, 36, 16, 198, 154, 7, 202, 69, 142, 189, 22, 76, 186, 14, 113, 231, 184, 236, 88, 49, 242, 120, 28, 152, 172, 173, 101, 8, 83, 92, 203, 248, 48, 66, 255, 131, 110, 216, 186, 114, 148, 117, 134, 86, 199, 127, 152, 28, 36, 106, 226, 251, 149, 104, 211, 14, 27, 214, 128, 128, 166, 117, 205, 71, 148, 66, 234, 231, 236, 10, 146, 156, 37, 129, 32, 67, 178, 154, 186, 52, 160, 192, 42, 64, 171, 129, 105, 105, 83, 250, 125, 51, 189, 179, 169, 106, 99, 127, 210, 241, 31, 78, 155, 26, 209, 130, 209, 225, 82, 69, 209, 161, 244, 76, 251, 49, 62, 74, 109, 232, 163, 51, 44, 85, 33, 95, 173, 65, 158, 7, 163, 196, 29, 162, 4, 58, 45, 22, 227, 7, 219, 13, 222, 18, 136, 241, 9, 136, 15, 123, 182, 74, 77, 27, 22, 179, 220, 237, 196, 144, 101, 77, 115, 141, 5, 48, 147, 135, 200, 69, 230, 3, 109, 20, 51, 62, 86, 146, 237, 205, 141, 168, 32, 73, 254, 233, 42, 83, 202, 164, 117, 202, 96, 253, 221, 232, 111, 175, 197, 38, 196, 204, 14, 212, 248, 64, 175, 208, 211, 67, 252, 233, 163, 191, 117, 64, 185, 30, 171, 70, 168, 177, 111, 248, 183, 249, 200, 17, 0, 171, 92, 122, 231, 18, 144, 255, 24, 231, 147, 222, 202, 16, 47, 137, 71, 207, 169, 58, 253, 25, 97, 140, 60, 220, 58, 44, 211, 135, 79, 28, 140, 172, 179, 149, 197, 186, 71, 104, 91, 0, 247, 41, 104, 140, 155, 217, 178, 53, 140, 131, 101, 237, 57, 192, 61, 65, 120, 32, 2, 82, 247, 43, 7, 108, 118, 206, 246, 63, 75, 42, 73, 244, 72, 109, 158, 1, 229, 138, 169, 144, 236, 253, 197, 179, 114, 254, 203, 64, 123, 231, 204, 6, 144, 216, 45, 0, 137, 128, 7, 164, 204, 171, 227, 85, 160, 152, 3, 66, 91, 36, 164, 157, 56, 147, 58, 177, 84, 146, 207, 120, 134, 141, 53, 162, 234, 236, 98, 51, 105, 1, 234, 99, 79, 98, 137, 207, 154, 7, 210, 67, 138, 20, 238, 204, 63, 67, 249, 131, 216, 26, 85, 201, 26, 147, 162, 12, 229, 100, 243, 103, 139, 190, 198, 180, 120, 68, 146, 238, 240, 176, 128, 245, 198, 151, 148, 53, 87, 130, 66, 18, 88, 248, 193, 135, 237, 77, 19, 21, 229, 249, 50, 58, 246, 216, 9, 122, 39, 248, 17, 95, 198, 201, 169, 143, 79, 137, ]#--------------------------------------------------------------------------------
		encrypted_payload = open('./license').read()

		# Key
		encryption_key = [127, 194, 34, 166, 139, 10, 252, 13, 12, 33, 62, 156, 32, 156, 23, 161]

		# Decrypt public key
		iv = encrypted_public_key[0:16]
		temp = b''
		for c in iv:
			temp += chr(c)
		iv = temp

		temp = b''
		for c in encryption_key:
			temp += chr(c)
		encryption_key = temp

		encrypted_public_key = encrypted_public_key[16:]
		temp = b''
		for c in encrypted_public_key:
			temp += chr(c)
		encrypted_public_key = temp

		cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
		public_key = cipher.decrypt(encrypted_public_key)

		# Decrypt license
		iv = encrypted_payload[0:16]
		temp = b''
		for c in iv:
			temp += c
		iv = temp

		temp = b''
		for c in encrypted_payload[16:]:
			temp += c
		encrypted_payload = temp

		cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
		payload = cipher.decrypt(encrypted_payload)
		
		iv = payload[0:16]
		signature = payload[16:272]
		license = payload[272:]

		# Verify License
		key = RSA.importKey(public_key)
		h = SHA.new(license)
		verifier = PKCS1_v1_5.new(key)
		if not verifier.verify(h, signature):
			sys.exit(1)
		else:
			check1 = '0876677837'
		license = json.loads(license)

		# Check for revocation
		conn = httplib.HTTPSConnection(license['host'])
		conn.request("GET", license['path'] + license['id'])
		r1 = conn.getresponse()
		date = r1.getheader('date')
		conn.close()
		if r1.status != 200:
			sys.exit(2)
		else:
			check2 = '2668052645'

		# Check expiration
		current_time = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
		current_time = time.mktime(current_time.timetuple())
		if current_time > license['expiration']:
			request = urllib.urlencode({'name': license['name'], 'id': license['id']})
			conn.request("GET", license['path'] + '/expired?' + request)
			r1 = conn.getresponse()
			sys.exit(3)
		else:
			check3 = '4818532868'

		# Check node
		node = uuid.getnode()
		try:
			license['nodes'].index(node)
			check4 = '5794981726'
		except:
			request = urllib.urlencode({'name': license['name'], 'node': node})
			conn.request("GET", license['path'] + '/unauthorized?' + request)
			r1 = conn.getresponse()
			print(node)
			sys.exit(4)

		assert check1 == '0876677837'
		assert check2 == '2668052645'
		assert check3 == '4818532868'
		assert check4 == '5794981726'

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
