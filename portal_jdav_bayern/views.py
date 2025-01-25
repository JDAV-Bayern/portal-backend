
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def admin_permission_denied(request: HttpRequest) -> HttpResponse:
    return render(request, 'permission_denied.html')