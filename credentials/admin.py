from django.contrib import admin

# Register your models here.
from .models import Profile
from .models import Organization
from .models import Volunteer
from .models import Event

admin.site.register(Profile)
admin.site.register(Organization)
admin.site.register(Volunteer)
admin.site.register(Event)