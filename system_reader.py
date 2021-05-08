import psutil
import time
from time import localtime, strftime
import json

def get_cpu_reading():
	cpu = {} #we will store the cpu readings here
	cpu_readings = psutil.cpu_percent(interval=1, percpu=True)

	for i in range(0,len(cpu_readings)):
		cpu['cpu'+str(i)] = cpu_readings[i] 

	return cpu


while True:

	reading_time = strftime("%H:%M:%S", localtime())

	time.sleep(1)#sleep for 1 second

	send_obj = {"time":reading_time, "cpu":get_cpu_reading()}

	print(json.dumps(send_obj))