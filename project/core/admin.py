from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class CustomUserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreateForm, self).__init__(*args, **kwargs)

        self.fields['password1'].required = False
        self.fields['password2'].required = False

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreateForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email'),
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'created_by', 'company', 'submission_date', 'ip_addr')
    list_display_links = ('title', 'rating', 'created_by', 'company', 'submission_date', 'ip_addr')
    search_fields = ('title', 'rating', 'submission_date', 'ip_addr')
    list_per_page = 25

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Company)
