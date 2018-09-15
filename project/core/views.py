from rest_framework import generics
from rest_framework import permissions

from .models import *
from .serializers import *


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(created_by=user)