import os
import requests
from pymongo import MongoClient
import time

api_url = os.environ.get('API_URL', 'http://localhost:8000')

total_mem = requests.get(f'{api_url}/hardware/memory').json()
total_disk = requests.get(f'{api_url}/hardware/disks').json()['disks']

host = os.environ.get('MONGO_HOST', 'localhost')
port = os.environ.get('MONGO_PORT', 27017)
username = os.environ.get('MONGO_USERNAME', 'root')
password = os.environ.get('MONGO_PASSWORD', 'example')
db_name = os.environ.get('MONGO_DB', 'malware')

client = MongoClient(host=host, port=port, username=username, password=password)
db = client[db_name]
collection = db['monitor']

while True:
    # get cpu usage
    data = {}

    rt_cpu_usage = requests.get(f'{api_url}/realtime/cpu').json()
    rt_mem_usage = requests.get(f'{api_url}/realtime/mem').json()
    rt_disk_usage = requests.get(f'{api_url}/realtime/disks').json()['disks']

    data['timestamp'] = int(time.time())
    data['ip'] = requests.get(f'{api_url}/platform/ip').json()

    data['cpu'] = rt_cpu_usage
    data['memory'] = {
        'used': rt_mem_usage['usage'],
        'total': total_mem['memory'],
        'precent': round((rt_mem_usage['usage'] / total_mem['memory']) * 100, 1)
    }
    data['disks'] = []


    for disk, rt_disk in zip(total_disk, rt_disk_usage):
        mountpoint = disk['mountpoint']
        max_capacity = disk['size']
        used_capacity = rt_disk['usage']
        disk_data = {
            'mountpoint': mountpoint,
            'used': used_capacity,
            'total': max_capacity,
            'precent': round((used_capacity / max_capacity) * 100, 1)
        }

        data['disks'].append(disk_data)

    print(data)
    document = collection.insert_one(data)

    time.sleep(1)