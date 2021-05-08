import psutil
import time
from time import localtime, strftime
import json
import asyncio
import websockets
import os

def get_cpu_reading():
	cpu = {} #we will store the cpu readings here
	cpu_readings = psutil.cpu_percent(interval=1, percpu=True)

	#{"cpu0": 52.5, "cpu1": 33.0, "cpu2": 54.5, "cpu3": 35.0}
	for i in range(0,len(cpu_readings)):
		cpu['cpu'+str(i)] = cpu_readings[i] 

	return cpu

def get_load_averages():
	load_avg = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
	mapped_avg = {"one_min":load_avg[0], "five_min":load_avg[1], "fifteen_min":load_avg[2]}
	return mapped_avg

def get_disk_uitilization_averages():
	disk_uitilization = psutil.disk_usage(os.getcwd())
	mapped_uitilization = disk_uitilization[0]%5
	return mapped_uitilization

def get_memory_averages():
	process = psutil.Process(os.getpid())
	mapped_process = process.memory_info()[0]%5
	return mapped_process


async def hello(websocket, path):
    name = await websocket.recv()
    time.sleep(1)#sleep for 1 second
    reading_time = strftime("%H:%M:%S", localtime())
    send_obj = json.dumps({"time":reading_time,\
    					   "cpu":get_cpu_reading(),\
    					   "load_avg":get_load_averages(),\
    					   "disk_utilized":get_disk_uitilization_averages(),\
    					   "memory_averages":get_memory_averages()})

    await websocket.send(send_obj)
    print(send_obj)

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()