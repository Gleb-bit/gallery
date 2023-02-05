from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from .models import User


class IsActivated(BasePermission):
    def has_permission(self, request, view):
        if (request.method != 'PATCH'):
            if 'email' in request.data:
                email = request.data['email'] if 'email' in request.data else ''
                try:
                    user = User.objects.get(email=email)
                except ObjectDoesNotExist:
                    return {"error": {"auth": "incorrect credentials"}}
                return user.is_verified

            return {"error": {"email": "field required"}}
        else:
            return True
