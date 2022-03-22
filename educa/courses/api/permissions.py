from rest_framework import permissions

class IsTeacher(permissions.BasePermission):

    def has_permission(self, request,view):
        if request.user.is_authenticated:
            return request.user.is_teacher
        return False

class IsStudent(permissions.BasePermission):

    def has_permission(self, request,view):
        if request.user.is_authenticated:
            return request.user.is_student
        return False