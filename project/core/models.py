import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


RATINGS = [('1',1),('2',2),('3',3),('4',4),('5',5)]


class Company(models.Model):
    name = models.CharField(max_length=255)


class Review(models.Model):
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10000)
    rating = models.IntegerField(choices=RATINGS)
    ip_addr = models.CharField(max_length=39, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, related_name='reviews', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.SET_NULL, null=True)