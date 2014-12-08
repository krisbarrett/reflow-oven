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

class ReflowController:
	def __init__(self):
		#--------------------------------------------------------------------------------
		# encrypted_payload and encrypted_public_key
		#--------------------------------------------------------------------------------
		encryption_key = [127, 194, 34, 166, 139, 10, 252, 13, 12, 33, 62, 156, 32, 156, 23, 161]
		encrypted_payload = [251, 179, 253, 44, 48, 173, 4, 54, 180, 199, 189, 61, 110, 43, 32, 72, 33, 45, 58, 196, 23, 34, 97, 134, 204, 112, 227, 201, 69, 36, 12, 2, 79, 149, 87, 43, 99, 9, 229, 126, 13, 140, 145, 116, 196, 174, 122, 64, 121, 61, 67, 189, 80, 116, 15, 143, 196, 221, 101, 80, 7, 38, 246, 204, 8, 127, 252, 124, 176, 38, 89, 221, 140, 109, 94, 70, 235, 163, 224, 229, 179, 48, 80, 9, 5, 90, 53, 36, 23, 107, 130, 87, 104, 89, 242, 25, 3, 58, 170, 90, 79, 78, 255, 137, 54, 172, 143, 222, 36, 237, 19, 218, 150, 224, 0, 129, 78, 203, 207, 5, 217, 248, 84, 64, 77, 57, 236, 36, 27, 21, 234, 255, 35, 72, 16, 169, 99, 30, 169, 45, 75, 106, 74, 13, 209, 213, 22, 18, 150, 193, 29, 166, 113, 89, 186, 5, 120, 173, 122, 82, 146, 78, 177, 64, 65, 199, 47, 188, 62, 99, 141, 117, 84, 115, 94, 210, 170, 7, 98, 95, 184, 53, 39, 176, 214, 78, 215, 232, 104, 213, 79, 136, 147, 28, 30, 173, 235, 102, 108, 42, 208, 100, 222, 75, 242, 114, 141, 209, 44, 43, 67, 214, 151, 110, 131, 60, 203, 127, 186, 183, 233, 157, 45, 221, 21, 221, 78, 255, 227, 14, 105, 40, 135, 50, 189, 68, 214, 190, 232, 144, 165, 193, 214, 53, 72, 222, 152, 201, 30, 255, 185, 120, 131, 206, 208, 3, 164, 43, 172, 8, 166, 168, 231, 176, 218, 136, 97, 237, 247, 240, 247, 178, 208, 30, 67, 17, 206, 108, 185, 131, 127, 40, 151, 97, 39, 130, 37, 186, 63, 163, 184, 124, 208, 149, 249, 113, 128, 52, 140, 183, 189, 148, 231, 80, 247, 241, 70, 120, 123, 105, 76, 184, 218, 212, 57, 166, 94, 211, 35, 203, 140, 174, 83, 173, 133, 187, 211, 42, 193, 234, 92, 21, 0, 225, 49, 101, 99, 46, 227, 239, 215, 1, 89, 21, 131, 43, 157, 251, 183, 225, 86, 225, 150, 174, 105, 6, 67, 88, 31, 151, 237, 115, 237, 47, 148, 164, 133, 156, 237, 112, 155, 77, 62, 66, 49, 166, 209, 197, 55, 101, 86, 166, 11, 117, 157, 32, 89, 59, 71, 189, 86, 108, 206, 130, 196, 86, 232, 21, 174, 160, 174, 13, 197, 113, 155, 64, 14, 1, 250, 76, 121, 171, 123, 188, 246, 254, 60, 238, 78, 194, 81, 144, 204, 231, 186, 34, 252, 176, 33, 102, 136, 111, 245, 250, 46, 218, 173, 64, 36, 68, 87, 226, 10, 2, 82, 226, 63, 40, 223, 242, 136, 4, ]
		encrypted_public_key = [82, 188, 242, 235, 51, 22, 165, 172, 8, 168, 51, 229, 227, 200, 40, 36, 122, 227, 206, 253, 210, 95, 103, 215, 204, 226, 127, 229, 143, 46, 88, 52, 36, 16, 198, 154, 7, 202, 69, 142, 189, 22, 76, 186, 14, 113, 231, 184, 236, 88, 49, 242, 120, 28, 152, 172, 173, 101, 8, 83, 92, 203, 248, 48, 66, 255, 131, 110, 216, 186, 114, 148, 117, 134, 86, 199, 127, 152, 28, 36, 106, 226, 251, 149, 104, 211, 14, 27, 214, 128, 128, 166, 117, 205, 71, 148, 66, 234, 231, 236, 10, 146, 156, 37, 129, 32, 67, 178, 154, 186, 52, 160, 192, 42, 64, 171, 129, 105, 105, 83, 250, 125, 51, 189, 179, 169, 106, 99, 127, 210, 241, 31, 78, 155, 26, 209, 130, 209, 225, 82, 69, 209, 161, 244, 76, 251, 49, 62, 74, 109, 232, 163, 51, 44, 85, 33, 95, 173, 65, 158, 7, 163, 196, 29, 162, 4, 58, 45, 22, 227, 7, 219, 13, 222, 18, 136, 241, 9, 136, 15, 123, 182, 74, 77, 27, 22, 179, 220, 237, 196, 144, 101, 77, 115, 141, 5, 48, 147, 135, 200, 69, 230, 3, 109, 20, 51, 62, 86, 146, 237, 205, 141, 168, 32, 73, 254, 233, 42, 83, 202, 164, 117, 202, 96, 253, 221, 232, 111, 175, 197, 38, 196, 204, 14, 212, 248, 64, 175, 208, 211, 67, 252, 233, 163, 191, 117, 64, 185, 30, 171, 70, 168, 177, 111, 248, 183, 249, 200, 17, 0, 171, 92, 122, 231, 18, 144, 255, 24, 231, 147, 222, 202, 16, 47, 137, 71, 207, 169, 58, 253, 25, 97, 140, 60, 220, 58, 44, 211, 135, 79, 28, 140, 172, 179, 149, 197, 186, 71, 104, 91, 0, 247, 41, 104, 140, 155, 217, 178, 53, 140, 131, 101, 237, 57, 192, 61, 65, 120, 32, 2, 82, 247, 43, 7, 108, 118, 206, 246, 63, 75, 42, 73, 244, 72, 109, 158, 1, 229, 138, 169, 144, 236, 253, 197, 179, 114, 254, 203, 64, 123, 231, 204, 6, 144, 216, 45, 0, 137, 128, 7, 164, 204, 171, 227, 85, 160, 152, 3, 66, 91, 36, 164, 157, 56, 147, 58, 177, 84, 146, 207, 120, 134, 141, 53, 162, 234, 236, 98, 51, 105, 1, 234, 99, 79, 98, 137, 207, 154, 7, 210, 67, 138, 20, 238, 204, 63, 67, 249, 131, 216, 26, 85, 201, 26, 147, 162, 12, 229, 100, 243, 103, 139, 190, 198, 180, 120, 68, 146, 238, 240, 176, 128, 245, 198, 151, 148, 53, 87, 130, 66, 18, 88, 248, 193, 135, 237, 77, 19, 21, 229, 249, 50, 58, 246, 216, 9, 122, 39, 248, 17, 95, 198, 201, 169, 143, 79, 137, ]#--------------------------------------------------------------------------------

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
			temp += chr(c)
		iv = temp

		temp = b''
		for c in encrypted_payload[16:]:
			temp += chr(c)
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
