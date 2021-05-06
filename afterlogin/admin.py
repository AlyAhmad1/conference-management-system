from django.contrib import admin
from .models import CfpData, AuthorData, ConferenceData, Reviews
# Register your models here.

admin.site.register(CfpData)
admin.site.register(AuthorData)
admin.site.register(ConferenceData)
admin.site.register(Reviews)
