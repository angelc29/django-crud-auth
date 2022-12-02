from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from .models import Task

# Se definen los campos que van a ser exportados con la libreria
# La sintaxis es parecida a los forms de django
class TaskResources(resources.ModelResource):
    class Meta:
        model = Task
        fields = ('title', 'description', 'important', 'datecompleted', 'id')

# Se remplaza admin.ModelAdmin por ImportExportModelAdmin
class TaskAdmin(ImportExportModelAdmin):
    resource_class = TaskResources
    readonly_fields = ("created",)


# Register your models here.
# Registra los modelos para poder ser utilizados en el panel del admin
admin.site.register(Task, TaskAdmin)