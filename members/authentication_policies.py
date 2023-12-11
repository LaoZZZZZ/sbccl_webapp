from rest_framework.authentication import BaseAuthentication


class MemberAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        return (request.user, request.auth)