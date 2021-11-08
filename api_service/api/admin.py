from django.contrib.admin import site

from api.models import UserRequestHistory

# Register your models here.
site.register(UserRequestHistory)
