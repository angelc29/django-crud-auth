from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
# Registra los modelos para poder ser utilizados en el panel del admin
admin.site.register(Task, TaskAdmin)