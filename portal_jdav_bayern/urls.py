"""
URL configuration for portal_jdav_bayern project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import include, path, reverse
from django.views import View
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from portal_jdav_bayern import settings
from portal_jdav_bayern.views import admin_permission_denied

class OIDCAdminLoginRedirect(View):
    def get(self, request, **kwargs):
        return HttpResponseRedirect(
            reverse('oidc_authentication_init') + (
                '?next={}'.format(request.GET['next']) if 'next' in request.GET else ''
            )
        )



urlpatterns = [
    path('api/', include('contact_info.urls')),
    path('api/', include('sections.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('reimbursements.urls')),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path('admin/login/', OIDCAdminLoginRedirect.as_view()),
    path('permission-denied', admin_permission_denied, name='admin_permission_denied'),
    path('admin/', admin.site.urls),
]

if settings.ENVIRONMENT == settings.Environments.DEVELOPMENT:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]




admin.site.site_header = 'Verwaltungsportal'
admin.site.site_title = 'JDAV Bayern Verwaltungsportal'
