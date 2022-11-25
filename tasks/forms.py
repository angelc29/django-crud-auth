from django.forms import ModelForm
from .models import Task

# Es la declaracion de formularios que se va encargar de hacer Django
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important'] # Se especifican los campos que se van a usar