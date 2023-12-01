# Retrieve 
from .models import Student

class UserInfoRetriever:
    # user: variable in user type.
    def __init__(self, user):
        self.user_info = user

    def get_students_by_parents(self):
        try:
          students = Student.objects.get(parent_id=self.user_info)              
        except Student.DoesNotExist:
            return []
        return students

    