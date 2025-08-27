from django.urls import path
from . import views  # ¡Esta línea es crucial!

urlpatterns = [
    path('', views.list_tasks, name='list-tasks'),
    path('create/', views.create_task, name='create-task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit-task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete-task'),
    path('send-email/', views.send_email_view, name='send-email'),
]