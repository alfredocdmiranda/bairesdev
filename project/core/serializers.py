from rest_framework import serializers

from .models import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company


class ReviewSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(source='company', queryset=Company.objects.all(), )

    class Meta:
        model = Review