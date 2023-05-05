from django.contrib import admin

from .models import PassModel
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(PassModel)
class PassData(ImportExportModelAdmin):
    pass