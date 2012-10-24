#TODO: Implement serial port selector
#TODO: Integrate temperature controller

from Tkinter import *
from threading import *
from random import *
from profile_widget import ProfileWidget
from reflow import Reflow
from temperature_controller import TemperatureController
import os
import re
import time

files = os.listdir("/dev")
serial_ports = []
serial_ports.append("-")
for f in files:
	match = re.search("tty[\.U]", f)
	if match != None:
		serial_ports.append(f)
	

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
	temp_controller = TemperatureController("/dev/" + serial_var.get())
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
serial_var = StringVar(root)
serial_var.set(serial_ports[0])
serial_option = apply(OptionMenu, (frame, serial_var) + tuple(serial_ports))
serial_label.grid(row=1, column=0)
serial_option.grid(row=1, column=1)

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