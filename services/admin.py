from django.contrib import admin
import subprocess
from services.views import ServiceSerializer
from elasticsearch import Elasticsearch
from django.conf import settings

from .models import *
from .views import *

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'publish', 'name')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_index()

admin.site.register(Service, ServiceAdmin)
admin.site.register(Age)
admin.site.register(Classification)
admin.site.register(Immigration)
admin.site.register(Duration)
admin.site.register(Health)
admin.site.register(Target)
admin.site.register(Study)
admin.site.register(ServicePath)
admin.site.register(Integration)

