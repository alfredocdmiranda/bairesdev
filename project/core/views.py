from rest_framework import generics
from rest_framework import permissions

from .models import *
from .serializers import *
from .helpers import get_client_ip_addr
from .permissions import IsOwnerOrSuperUser


class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return CompanySerializer


class ReviewList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(created_by=user)

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return ReviewSerializer

    def perform_create(self, serializer):
        ip_addr = get_client_ip_addr(self.request)
        serializer.save(created_by=self.request.user, ip_addr=ip_addr)


class ReviewDetails(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrSuperUser)

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return ReviewSerializer