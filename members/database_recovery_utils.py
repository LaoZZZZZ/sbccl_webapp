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
            student_reg = parent_account.get(row['student'].strip().lower(), [])
            student_reg.append(row)
            total_registration += 1
            language_registration += 1
        with open(registration_detail_file, newline='') as raw_registration:
            raw_reader = csv.DictReader(raw_registration)
            for row in raw_reader:
                if row['email'].strip().lower() in temp_map:
                    per_account_regs = temp_map[row['email'].strip().lower()]
                    matched_student_regs = per_account_regs.get(row['student'].lower().strip(), [])
                    if not matched_student_regs:
                        print("Extra student: ", row)
                        matched_student_regs.append(row)
                        continue
                    # It's a language class.
                    if len(row['class'].strip()) > 4: # enrichment class
                        matched_student_regs.append(row)
                        total_registration += 1
                    else:

                        # if len(row['class']) <= 3 and matched_student[0]['class'] != row['class']:
                        #     print("mismatched class for a student: ", row, matched_student)
                        matched_reg = None
                        for r in matched_student_regs:
                            if r['class'].strip() == row['class'].strip():
                                matched_reg = r
                                break
                            elif r['class'].strip()[:2] == row['class'].strip()[:2]:
                                # it's a class re-assignment
                                matched_reg = r
                                break
                            else:
                                # totally different registration
                                continue
                        if matched_reg:
                            matched_reg['registration_code'] = row['registration_code'].strip()
                            matched_reg['registration_date'] = row['registration_date'].strip()
                            matched_reg['status'] = 'Enrolled'
                            matched_reg['balance'] = row['balance'].strip()
                            matched_reg['book_order'] = row['book_order'].strip()
                        else:
                            print('omitted registration:', matched_student_regs)
                else:
                    print("new account:", row)
                    new_registrations += 1
        result = []
        for k, v in temp_map.items():
            regs = []
            for s, r in v.items():
                regs += r
            result.append({'email': k, 'registrations': regs})
        return result



def call_add_teacher_api(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json, text/plain, */*'}

    teachers = {'teachers': data}
    resp = requests.put(url, data=json.dumps(teachers), headers=headers, auth=HTTPBasicAuth('luzhao1986@gmail.com', 'Sandy@2013'))
    print(resp.text)

def call_add_registration_api(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json, text/plain, */*'}

    registrations = {'registrations': data}
    resp = requests.put(url, data=json.dumps(registrations), headers=headers, auth=HTTPBasicAuth('luzhao1986@gmail.com', 'Sandy@2013'))
    print(resp.json())

if __name__ == '__main__':
    url = 'http://prod.api.sbcclny.com/rest_api/members/batch-add-teachers/'
    dev_url = 'http://localhost:8000/rest_api/members/batch-add-teachers/'
    filename = '/Users/luzhao/Downloads/teacher_information.csv'
    # call_add_teacher_api(url, load_csv(filename))
    language_roster_file = '/Users/luzhao/Downloads/student_language_registration.csv'
    raw_roster_file = '/Users/luzhao/Downloads/recovered_registration.csv'
    registration_data = parse_registration_page(raw_roster_file, language_roster_file)

    url = 'http://prod.api.sbcclny.com/rest_api/members/batch-add-registrations/'
    dev_url = 'http://localhost:8000/rest_api/members/batch-add-registrations/'
    call_add_registration_api(dev_url, registration_data)
