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

def parse_registration_page(registration_detail_file, language_roster_file):
    # need to handle language and enrichment class separately as 
    language_registrations = []
    enrichment_registrations = []
    with open(language_roster_file, newline='') as language:
        reader = csv.DictReader(language)
        temp_map = dict()
        total_registration = 0
        language_registration = 0
        new_registrations = 0
        # Combine students under a parent account.
        for row in reader:
            if row['email'] == '':
                continue
            temp_map.setdefault(row['email'].strip().lower(), {})
            parent_account = temp_map.get(row['email'].strip().lower(), {})
            parent_account.setdefault(row['student'].lower().strip(), [])
            student_reg = parent_account.get(row['student'].lower().strip(), [])
            student_reg.append(row)
            total_registration += 1
            language_registration += 1
        with open(registration_detail_file, newline='') as raw_registration:
            raw_reader = csv.DictReader(raw_registration)
            for row in raw_reader:
                if row['email'].strip().lower() in temp_map:
                    matched_student = temp_map[row['email'].strip().lower()].get(row['student'].lower().strip(), [])
                    if not matched_student:
                        print("Extra registration: ", row)
                        matched_student.append(row)
                        continue
                    # It's a language class.
                    if len(row['class']) <= 3 and matched_student[0]['class'] != row['class']:
                        print("mismatched class for a student: ", row, matched_student)
                    elif len(row['class']) > 3: # enrichment class
                        matched_student.append(row)
                        total_registration += 1
                    else:
                        matched_student[0]['registration_code'] = row['registration_code']
                        matched_student[0]['registration_date'] = row['registration_date']
                        matched_student[0]['status'] = row['status']
                        matched_student[0]['balance'] = row['balance']
                        matched_student[0]['book_order'] = row['book_order']
                else:
                    print("new registration:", row)
                    new_registrations += 1
        print(len(temp_map), total_registration, language_registration, new_registrations)



def call_add_teacher_api(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json, text/plain, */*'}

    teachers = {'teachers': data}
    resp = requests.put(url, data=json.dumps(teachers), headers=headers, auth=HTTPBasicAuth('luzhao1986@gmail.com', 'Sandy@2013'))
    print(resp)

if __name__ == '__main__':
    url = 'http://prod.api.sbcclny.com/rest_api/members/batch-add-teachers/'
    dev_url = 'http://localhost:8000/rest_api/members/batch-add-teachers/'
    filename = '/Users/luzhao/Downloads/teacher_information.csv'
    # call_add_teacher_api(url, load_csv(filename))
    language_roster_file = '/Users/luzhao/Downloads/student_language_registration.csv'
    raw_roster_file = '/Users/luzhao/Downloads/recovered_registration.csv'
    parse_registration_page(raw_roster_file, language_roster_file)
