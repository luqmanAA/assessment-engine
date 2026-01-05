from rest_framework.permissions import BasePermission


class IsOwnerOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # The 'obj' here is the Submission instance.
        # Check if the student associated with the submission is the request.user.
        print("request method: ", request.method)
        return request.method != 'POST' and obj.student == request.user