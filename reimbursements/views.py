from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny

from reimbursements.models import  Reimbursement
from reimbursements.serializers import ReimbursementSerializer


class ReimbursementList(generics.ListCreateAPIView):
    queryset = Reimbursement.objects.all()
    serializer_class = ReimbursementSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
