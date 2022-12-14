from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True) # Se le agrega blank para no ser dato requerido en el administrador
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Sirve para dar una mejor visualizacion desde el panel del admin
    def __str__(self):
        return self.title + ' - by ' + self.user.username