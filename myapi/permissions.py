from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Uncomment this if you want everyone to be able to see everybody's runs
        # if request.method in permissions.SAFE_METHODS: # Setting
        #     return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
