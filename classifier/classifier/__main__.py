import os
import requests
import time
from pymongo import MongoClient
import mimetypes
from requests_toolbelt.multipart.encoder import MultipartEncoder
from tqdm.auto import tqdm
import glob
import hashlib

api_url = os.environ.get('API_URL', 'http://localhost:8000')
file_dir = os.environ.get('DATA_DIR', '/data')

host = os.environ.get('MONGO_HOST', 'localhost')
port = os.environ.get('MONGO_PORT', 27017)
username = os.environ.get('MONGO_USERNAME', 'root')
password = os.environ.get('MONGO_PASSWORD', 'example')
db_name = os.environ.get('MONGO_DB', 'malware')

client = MongoClient(host=host, port=port, username=username, password=password)
db = client[db_name]
collection = db['malware']

initial_files = []

count = 0
while True:
    try:
        print(file_dir)
        current_files = glob.glob(file_dir + '/*')

        new_files = set(current_files) - set(initial_files)

        if new_files:
            print(len(current_files))
            for file in tqdm(new_files):
                print(file)
                files = {'file': (file, open(os.path.join(file_dir, file), 'rb'))}

                uploaded_path = requests.post(f'{api_url}/scan/upload', files=files).json()['path']

                result = {}

                result['timestamp'] = int(time.time())
                result['ip'] = requests.get(f'{api_url}/platform/ip').json()
                # result['id'] = hashlib.sha256(open(os.path.join(file_dir, file), 'rb').read()).hexdigest()
                result['fileinfo'] = requests.get(f'{api_url}/scan/info', params={'path': uploaded_path}).json()
                # result['virustotal'] = requests.get(f'{api_url}/scan/vt', params={'path': uploaded_path}).json()
                # result['malwarebazaar'] = requests.get(f'{api_url}/scan/mb', params={'path': uploaded_path}).json()
                result['prediction'] = requests.get(f'{api_url}/scan/prediction', params={'path': uploaded_path}).json()

                # upload file to API
                document = collection.insert_one(result)

            initial_files = current_files
    except Exception as e:
        pass

    #     time.sleep(15) # Wait for 15sec (4 samples / min)
    #     count += 1
    # if count == 500:
    #     time.sleep(86400) # Sleep 24 hours
    #     count = 0