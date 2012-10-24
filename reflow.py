class Reflow:
	@staticmethod
	def reflow(starting_temp=25, preheat_min=100, preheat_max=150.0, 
	           peak_temp=215.0, flow_temp=183.0, ramp_up=2, ramp_down=1, 
	           preheat_time=90, peak_time=20, flow_time=90):
		
		temp = starting_temp
		time = 0
		result = []
		
		b = temp
		while(temp < preheat_min):
			temp = ramp_up * time + b
			time += 1
			warmup1_temp = temp
			warmup1_t = time
			if temp < preheat_min:
				result.append(temp)

		slope =	(preheat_max - preheat_min) / preheat_time
		b = warmup1_temp - slope * warmup1_t
		while(temp < preheat_max):
			temp = slope * time + b
			time += 1
			preheat_t = time
			if temp < preheat_max:
				result.append(temp)

		b = preheat_max - ramp_up * preheat_t
		while(time < peak_time):
			temp = ramp_up * time + b
			time += 1
			warmup2_temp = temp
			warmup2_t = time
			if time < peak_time:
				result.append(temp)

		flow2_time = peak_time
		flow3_time = (peak_temp - flow_temp) / ramp_down
		flow1_time = flow_time - flow2_time - flow3_time
		slope = (peak_temp - flow_temp) / flow1_time
		b = temp - slope * time
		while(temp < peak_temp):
			temp = slope * time + b
			time += 1
			flow1_t = time
			if temp < peak_temp:
				result.append(temp)

		while(time < flow1_t + peak_time):
			temp = peak_temp
			time += 1
			flow2_t = time
			if time < flow1_t + peak_time:
				result.append(temp)

		b = peak_temp + ramp_down * flow2_t
		while(temp > 50):
			temp = -ramp_down * time + b
			time += 1
			if temp > 50:
				result.append(temp)

		return result
