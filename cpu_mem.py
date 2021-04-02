import random
import time
import requests


def measureCpuMem():
	cpu = random.uniform(1, 8)
	mem = random.uniform(0.1, 1.1)
	#print("cpu: ", cpu)
	#print("mem: ", mem)
	cpu_json = {"instanceID": 1, "cpu": cpu}
	r1 = requests.put("http://localhost:5000/api/v1/results/cpu", json=cpu_json)
	ram_json = {"instanceID": 1, "ram": mem}
	r2 = requests.put("http://localhost:5000/api/v1/results/ram", json=ram_json)
	time.sleep(2)


