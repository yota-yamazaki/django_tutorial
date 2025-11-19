from django.contrib import admin
from mysite.admin import head_office_admin_site
from .models import Store, News

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

head_office_admin_site.register(Store)
head_office_admin_site.register(News)

head_office_admin_site.register(User, UserAdmin)
