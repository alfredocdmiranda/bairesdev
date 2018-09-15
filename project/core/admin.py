from django.contrib import admin

from .models import *


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'created_by', 'company', 'submission_date', 'ip_addr')
    list_display_links = ('title', 'rating', 'created_by', 'company', 'submission_date', 'ip_addr')
    search_fields = ('title', 'rating', 'submission_date', 'ip_addr')
    list_per_page = 25

# Register your models here.
admin.site.register(Company)
