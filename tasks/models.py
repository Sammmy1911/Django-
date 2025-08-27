from django.db import models


from django.db import migrations
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)
    new_field = models.CharField(max_length=100, default='Nuevo valor')  
def update_task_status(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    Task.objects.filter(status='Pendiente').update(status='En progreso')





class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Create your models here.

class Status(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False,
        blank=False,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name
    




class Task(models.Model):
    id = models.AutoField(
    primary_key=True,
    null=False,
    blank=False,
    )

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False,
    )
    
    deadline = models.DateTimeField(
        null=True,
        blank=True,
    )

    status_id = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name
    

    


    