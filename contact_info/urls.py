from django.urls import path

from contact_info import views


urlpatterns = [
    path('countries/', views.CountryList.as_view(), name='country-list'),
    path('localities/', views.LocalityList.as_view(), name='locality-list'),
]
