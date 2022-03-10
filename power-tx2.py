import sys 
import os
import json
import threading
from collections import deque
import time

import numpy as np
import statistics  
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
REGEXP = re.compile(r'(.+?): ((.*))')

class Analyser:
	
	t1 = threading.Thread
	start=False
	temporary_file = open("temporary_file.txt", "w+")
	
	def start_recording(self):
		self.t1 = threading.Thread(target=self.model_report) 
		self.t1.start()
		self.start = True
		
	def stop_recording(self):
		self.start = False
		self.t1.join()
 
	def model_report(self):
		gpu_list, cpu_list, cpu_list1, gpu_temp, cpu_temp, timer, list1, power_consumption_list = [], [], [], [], [], [], [], []
		
		def gpu_usage():	
			gpuLoadFile="/sys/devices/gpu.0/load"
			with open(gpuLoadFile, 'r') as gpuFile:
				gpuusage=gpuFile.read()
			gpu_value=float(gpuusage)/10
			return gpu_value

		def memory_usage():
			memoryLoadFile="/proc/meminfo"
			with open(memoryLoadFile) as fp:
				for i, line in enumerate(fp):
					if i == 2:
						memory_value=((8-((float(line[17])*10 + float(line[18]))/10))/8)*100
						break
			return memory_value
			
		#def cpu_usage():
		#	list_cpu2 = {}
		#	x=0
		#	cpuLoadFile="/proc/cpuinfo"
		#	with open(cpuLoadFile) as fp:
		#			for line in fp:
		#				# Search line
		#				match = REGEXP.search(line)
		#				if match:
		#					key = match.group(1).rstrip()
		#					value = match.group(2).rstrip()
		#					# Load value or if it is a new processor initialize a new field
		#				if key == "processor":
		#					idx = int(value) + 1
		#					name = "CPU{idx}".format(idx=idx)
		#					list_cpu2[name] = {}
		#					print(list_cpu2[name])
		#				else:
		#					# Load cpu info
		#					list_cpu2[name][key] = value
		#				cpu_free = x + float(value)
		#	return cpu_free

		def gpu_temperature():
			tempLoadFile="/sys/devices/virtual/thermal/thermal_zone2/temp"
			with open(tempLoadFile,'r') as tempFile:
				temp=tempFile.read()
			gpu_temp_value=float(temp)/1000
			return gpu_temp_value

		def cpu_temperature():
			tempLoadFile1="/sys/devices/virtual/thermal/thermal_zone1/temp"
			with open(tempLoadFile1,'r') as tempFile1:
				temp1=tempFile1.read()
			cpu_temp_value=float(temp1)/1000
			return cpu_temp_value
			
		def power_consumption():
			tempLoadFile5="/sys/bus/i2c/drivers/ina3221x/0-0041/iio:device1/in_power0_input"#IN(ALL) POWER
			with open(tempLoadFile5,'r') as tempFile5:
				temp5=tempFile5.read()

			power_value=float(temp5)
			return power_value
			
		while(True):
			if(self.start==True):
				break
			
		start_time=time.time()	
		i=0
		with open('temporary_file.txt', 'w+') as temporary_file_write:
			while (self.start):
				i=i+5
				temporary_file_write.write("%f\n%f\n%f\n%f\n%f\n"%(gpu_usage(),memory_usage(),gpu_temperature(),cpu_temperature(),power_consumption()))
				timer.append(time.time()-start_time)
			
		file= open("temporary_file.txt","r") 
		list1 = []
		value1=file.readlines()
		for value in value1:
			value=float(value)
			list1.append(value)
                
		i=0
		while(i<=len(list1)-5):
			gpu_list.append(list1[i])
			cpu_list.append(list1[i+1])
			gpu_temp.append(list1[i+2])
			cpu_temp.append(list1[i+3])
			power_consumption_list.append(list1[i+4])
			i=i+5	

			
		plt.subplot(3, 1, 1)
		plt.plot(timer, gpu_list,label='GPU Usage')
		plt.plot(timer, cpu_list,label='Memory Usage')	
		plt.title('Model Inference Report')
		plt.ylabel('Usage (%)')
		plt.title('AVG GPU usage: %f , Avg Memory Used: %f'%(statistics.mean(gpu_list),statistics.mean(cpu_list)))
		plt.legend()
		
		#plt.show()
		plt.subplot(3, 1, 2)
		plt.plot(timer, gpu_temp,label='GPU Temp')
		plt.plot(timer, cpu_temp,label='CPU Temp')
		
		plt.ylabel('Temperature')
		plt.title('Avg GPU temp: %f , Avg CPU Temp: %f'%(statistics.mean(cpu_temp),statistics.mean(gpu_temp)))
		plt.legend()
		
		#plt.show()
		plt.subplot(3,1,3)
		plt.plot(timer,power_consumption_list)
		plt.xlabel('time(s)')
		plt.ylabel('Power_consumption')
		plt.title('AVG Power consumed in: %f milliWatts'%statistics.mean(power_consumption_list))
		plt.subplots_adjust(left=None, bottom=None, right=1, top=None, wspace=None, hspace=1)
			
		plt.savefig('./model-tx23.png')

		#plt.show()

if __name__ == "__main__":
    analyser = Analyser()
    analyser.start_recording()
    time.sleep(15)
    analyser.stop_recording()
