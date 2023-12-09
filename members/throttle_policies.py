from rest_framework import UserRateThrottle

# Applied to login, password reset. Unauthenticated user
class UserUpdateThrottle(UserRateThrottle):
    rate = '3/minutes'

# At most sign up 5 account every day.
class UserSignUpThrottle(UserRateThrottle):
    rate = '5/day'

