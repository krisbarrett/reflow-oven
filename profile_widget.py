from Tkinter import *

class ProfileWidget():
	
	def to_pixelx(self, val):
		return val * self.width / (self.xmax - self.xmin)
	
	def to_pixely(self, val):
		return self.height - (val * self.height / (self.ymax - self.ymin))
		
	def add_actual(self, value):
		self.actual.append(value)
		if len(self.actual) > 2:
			i = len(self.actual) - 1
			self.canvas.create_line(self.to_pixelx(i-1), 
			                        self.to_pixely(self.actual[i-1]), 
			                        self.to_pixelx(i), 
			                        self.to_pixely(self.actual[i]),
			                        fill="red", width=3)
	def draw_gridx(self):
		for x in range(int(self.xmin), int(self.xmax), 10):
			self.canvas.create_line(self.to_pixelx(x), 
			                        self.to_pixely(self.ymin), 
			                        self.to_pixelx(x), 
			                        self.to_pixely(self.ymax),
			                        fill="gray", width=1)
			
	def draw_gridy(self):
		for y in range(int(self.ymin), int(self.ymax), 10):
			self.canvas.create_line(self.to_pixelx(self.xmin), 
			                        self.to_pixely(y), 
			                        self.to_pixelx(self.xmax), 
			                        self.to_pixely(y),
			                        fill="gray", width=1)
	
	def redraw(self):
		self.canvas.delete("all")
		
		self.actual = []
		
		self.desiredx = range(0, len(self.desired))
		
		# FIXME: Setting the minimums to anything other than 0, doesn't display correctly
		self.xmin = 0 #min(self.desiredx)
		self.xmax = max(self.desiredx) * 1.1
		self.ymin = 0 #min(self.desired)
		self.ymax = max(self.desired) * 1.1
		
		self.draw_gridx()
		self.draw_gridy()
		self.canvas.create_rectangle(3, 3, self.width, self.height, width=1)
		
		for i in range(0,len(self.desiredx)-1):
			self.canvas.create_line(self.to_pixelx(self.desiredx[i]), 
			                   self.to_pixely(self.desired[i]), 
			                   self.to_pixelx(self.desiredx[i+1]), 
			                   self.to_pixely(self.desired[i+1]),
			                   fill="gray", width=2)
			
			
	def sample_data(self):
		return [25.0, 27.0, 29.0, 31.0, 33.0, 35.0, 37.0, 39.0, 41.0, 43.0, 
		         45.0, 47.0, 49.0, 51.0, 53.0, 55.0, 57.0, 59.0, 61.0, 63.0, 
				 65.0, 67.0, 69.0, 71.0, 73.0, 75.0, 77.0, 79.0, 81.0, 83.0, 
				 85.0, 87.0, 89.0, 91.0, 93.0, 95.0, 97.0, 99.0, 101.0, 101.0, 
				 101.56, 102.11, 102.67, 103.22, 103.78, 104.33, 104.89, 105.44, 
				 106.0, 106.56, 107.11, 107.67, 108.22, 108.78, 109.33, 109.89, 
				 110.44, 111.0, 111.56, 112.11, 112.67, 113.22, 113.78, 114.33, 
				 114.89, 115.44, 116.0, 116.56, 117.11, 117.67, 118.22, 118.78, 
				 119.33, 119.89, 120.44, 121.0, 121.56, 122.11, 122.67, 123.22, 
				 123.78, 124.33, 124.89, 125.44, 126.0, 126.56, 127.11, 127.67, 
				 128.22, 128.78, 129.33, 129.89, 130.44, 131.0, 131.56, 132.11, 
				 132.67, 133.22, 133.78, 134.33, 134.89, 135.44, 136.0, 136.56, 
				 137.11, 137.67, 138.22, 138.78, 139.33, 139.89, 140.44, 141.0, 
				 141.56, 142.11, 142.67, 143.22, 143.78, 144.33, 144.89, 145.44, 
				 146.0, 146.56, 147.11, 147.67, 148.22, 148.78, 149.33, 149.89, 
				 150.44, 150.44, 151.29, 152.13, 152.97, 153.81, 154.65, 155.5, 
				 156.34, 157.18, 158.02, 158.87, 159.71, 160.55, 161.39, 162.23, 
				 163.08, 163.92, 164.76, 165.6, 166.44, 167.29, 168.13, 168.97, 
				 169.81, 170.65, 171.5, 172.34, 173.18, 174.02, 174.87, 175.71, 
				 176.55, 177.39, 178.23, 179.08, 179.92, 180.76, 181.6, 182.44, 
				 183.29, 184.13, 184.97, 185.81, 186.65, 187.5, 188.34, 189.18, 
				 190.02, 190.87, 191.71, 192.55, 193.39, 194.23, 195.08, 195.92, 
				 196.76, 197.6, 198.44, 199.29, 200.13, 200.97, 201.81, 202.65, 
				 203.5, 204.34, 205.18, 206.02, 206.87, 207.71, 208.55, 209.39, 
				 210.23, 211.08, 211.92, 212.76, 213.6, 214.44, 215.29, 215.0, 
				 215.0, 215.0, 215.0, 215.0, 215.0, 215.0, 215.0, 215.0, 215.0, 
				 215.0, 215.0, 215.0, 215.0, 215.0, 215.0, 215.0, 215.0, 215.0, 
				 215.0, 215.0, 214.0, 213.0, 212.0, 211.0, 210.0, 209.0, 208.0, 
				 207.0, 206.0, 205.0, 204.0, 203.0, 202.0, 201.0, 200.0, 199.0, 
				 198.0, 197.0, 196.0, 195.0, 194.0, 193.0, 192.0, 191.0, 190.0, 
				 189.0, 188.0, 187.0, 186.0, 185.0, 184.0, 183.0, 182.0, 181.0, 
				 180.0, 179.0, 178.0, 177.0, 176.0, 175.0, 174.0, 173.0, 172.0, 
				 171.0, 170.0, 169.0, 168.0, 167.0, 166.0, 165.0, 164.0, 163.0, 
				 162.0, 161.0, 160.0, 159.0, 158.0, 157.0, 156.0, 155.0, 154.0, 
				 153.0, 152.0, 151.0, 150.0, 149.0, 148.0, 147.0, 146.0, 145.0, 
				 144.0, 143.0, 142.0, 141.0, 140.0, 139.0, 138.0, 137.0, 136.0, 
				 135.0, 134.0, 133.0, 132.0, 131.0, 130.0, 129.0, 128.0, 127.0, 
				 126.0, 125.0, 124.0, 123.0, 122.0, 121.0, 120.0, 119.0, 118.0, 
				 117.0, 116.0, 115.0, 114.0, 113.0, 112.0, 111.0, 110.0, 109.0, 
				 108.0, 107.0, 106.0, 105.0, 104.0, 103.0, 102.0, 101.0, 100.0]
			
	def __init__(self, width, height):
		self.desired = []
		self.actual = []
		self.width = width
		self.height = height
		self.canvas = Canvas(width=width, height=height)
		self.canvas.create_rectangle(3, 3, self.width, self.height, width=1)



