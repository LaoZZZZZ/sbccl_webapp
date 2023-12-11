from rest_framework import permissions

class MemberPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # 100% access to super users
        if request.user.is_superuser:
            return True
        if view.action == 'sign-up':
            print("Resource permission grated")
            return True
        elif view.action == 'list':
            # Expose this API only to 
            return bool(IsOwner().has_permission(request, view)
                        or IsStaff().has_permission(request, view))
        else:
            return bool(request.user and request.user.is_authenticated)
     
    
class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False