from typing import Callable
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import Permission, User
from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse


class PermissionBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        email = claims.get("email")
        username = claims.get("sub")
        permClaim = (
            "urn:zitadel:iam:org:project:"
            + self.get_settings("ZITADEL_PROJECT")
            + ":roles"
        )

        permissions = claims.get(permClaim, [])

        if "admin" in permissions:
            user = self.UserModel.objects.create_user(
                username, email=email, is_superuser=True, is_staff=True
            )
            user.first_name = claims.get("given_name")
            user.last_name = claims.get("family_name")
            user.save()
            return user
        else: 
            user = self.UserModel.objects.create_user(username, email=email)
            user.first_name = claims.get("given_name")
            user.last_name = claims.get("family_name")
            user.save()
            return user

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name")
        user.last_name = claims.get("family_name")
        permClaim = (
            "urn:zitadel:iam:org:project:"
            + self.get_settings("ZITADEL_PROJECT")
            + ":roles"
        )

        permissions = claims.get(permClaim, [])

        if "admin" in permissions:
            user.is_superuser = True
            user.is_staff = True
            user.save()
        return user


class PreventAdminRedirectLoopMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Check if the request is for the admin page
        if request.path.startswith('/admin/'):
            if hasattr(request, 'user') and request.user.is_authenticated and not request.user.is_staff:
            # Redirect non-staff users to a custom page
                return HttpResponseRedirect(reverse('admin_permission_denied'))
        return self.get_response(request)
