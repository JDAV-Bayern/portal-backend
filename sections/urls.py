from django.urls import path

from sections import views


urlpatterns = [
    path('federations/', views.FederationList.as_view(), name='federation-list'),
    path('federations/<int:pk>/', views.FederationDetail.as_view(), name='federation-detail'),
    path('federations/<int:federation_id>/sections/', views.FederationSectionList.as_view(), name='federation-section-list'),
    path('sections/', views.SectionList.as_view(), name='section-list'),
    path('sections/<int:pk>/', views.SectionDetail.as_view(), name='section-detail'),
]
