from django.urls import path

from reimbursements import views


urlpatterns = [
    path('reimbursements', views.ReimbursementList.as_view(), name='course-reimbursement-list'),
]
