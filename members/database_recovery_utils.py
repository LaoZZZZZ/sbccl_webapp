import csv
import json
from requests.auth import HTTPBasicAuth
import requests


def load_csv(filename):
    with open(filename, newline='')  as csvfile:
        reader = csv.DictReader(csvfile)
        result = []
        for row in reader:
            result.append(row)
        return result

def call_add_teacher_api(data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json, text/plain, */*'}

    teachers = {'teachers': data}
    resp = requests.put('http://localhost:8000/rest_api/members/batch-add-teachers/',
                        data=json.dumps(teachers), headers=headers,
                        auth=HTTPBasicAuth('luzhao1986@gmail.com', 'Sandy@2013'))
    print(resp)

if __name__ == '__main__':
    filename = '/Users/luzhao/Downloads/teacher_information.csv'
    call_add_teacher_api(load_csv(filename))