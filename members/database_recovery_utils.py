import csv
import json
from requests.auth import HTTPBasicAuth
import requests
import sys, getopt

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
            email = row['email'].strip().lower().split(',')[0]
            temp_map.setdefault(email, {})
            parent_account = temp_map.get(email, {})
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
                        row['class'] = row['class'].strip()
                        matched_student_regs.append(row)
                        total_registration += 1
                    else:

                        # if len(row['class']) <= 3 and matched_student[0]['class'] != row['class']:
                        #     print("mismatched class for a student: ", row, matched_student)
                        matched_reg = None
                        for r in matched_student_regs:
                            r['class'] = r['class'].strip()
                            if r['class'] == row['class'].strip():
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
        total_registrations = 0
        for k, v in temp_map.items():
            regs = []
            for s, r in v.items():
                regs += r
            result.append({'email': k, 'registrations': regs})
            total_registrations += len(regs)
            if k == 'orient03@gmail.com':
                print(v)
        print("total registration:", total_registrations, language_registration)
        return result

def check_recovered_registration(registration_detail_file):
    with open(registration_detail_file, newline='') as raw_registration:
        raw_reader = csv.DictReader(raw_registration)
        for row in raw_reader:
            if row['email'] == '':
                print(row)
                continue
            if len(row['student'].split()) != 2:
                print(row)
                continue
            if row['class'] == '':
                print(row)
                continue
            if row['registration_code'] == '':
                print(row)
                continue
            if row['registration_date'] == '':
                print(row)
                continue
            if not row['status'] in ('Enrolled', 'On Waiting List', 'withdraw'):
                print(row)
                continue
            if row['balance'] == '':
                print(row)
                continue
            if not row['book_order'] in ('NA', 'Ordered', 'NotOrdered'):
                print(row)
                continue

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

def call_update_students_api(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json, text/plain, */*'}

    registrations = {'students': data}
    resp = requests.put(url, data=json.dumps(registrations), headers=headers, auth=HTTPBasicAuth('luzhao1986@gmail.com', 'Sandy@2013'))
    print(resp.json())

if __name__ == '__main__':
    api_url = ''
    input_file = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:u:o", ["url", "input_file"])
        for o, a in opts:
            if o in ('-u', '--url'):
                api_url = a                 
            elif o in ('-i', '--input_file'):
                input_file = a
    except getopt.GetoptError as e:
        print("Failed to parse provided parameters")
    
    if not api_url or not input_file:
        print("Missing required arguments!")

    if api_url.endswith('batch-add-teachers/'):
        print(input_file)
        call_add_teacher_api(api_url, load_csv(input_file))
    elif api_url.endswith('batch-add-registrations/'):
        intput_files = input_file.split(',')
        if len(intput_files) != 2:
            raise ValueError(f'Invalid input file: {input_file}')
        call_add_registration_api(api_url, intput_files[0], intput_files[1])
    elif api_url.endswith('batch-update-students/'):
        print(load_csv(input_file))
        call_update_students_api(api_url, load_csv(input_file))