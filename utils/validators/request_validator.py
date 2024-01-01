import re

def ValidateUser(user_info):
    pass

def ValidateStudent(student_info):
    pass

def ValidateBoardMember(board_member):
    pass

def ValidateUserEmail(email):
    pass

def ValidatePasswordFormat(password):
    pass

def ValidatePhoneNumber(phone_number):
    pattern = "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"
    return re.match(pattern, phone_number.strip())
