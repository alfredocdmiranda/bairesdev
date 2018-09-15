from rest_framework import serializers

from .models import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(source='company', queryset=Company.objects.all(), )
    created_by = serializers.CharField()

    class Meta:
        model = Review
        fields = '__all__'
