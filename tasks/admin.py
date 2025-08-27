from django.contrib import admin
from .models import Task, Status

# Asegúrate de que solo tengas UNA de estas líneas, no múltiples registros
admin.site.register(Task)
admin.site.register(Status)