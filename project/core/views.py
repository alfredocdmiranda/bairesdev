from rest_framework import generics
from rest_framework import permissions

from .models import *
from .serializers import *
from .helpers import get_client_ip_addr
from .permissions import IsOwnerOrSuperUser


class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class =  CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(created_by=user)

    def perform_create(self, serializer):
        ip_addr = get_client_ip_addr(self.request)
        serializer.save(created_by=self.request.user, ip_addr=ip_addr)


class ReviewDetails(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrSuperUser)