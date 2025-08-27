from django.shortcuts import render
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.models import Task, Status
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import login_required, user_passes_test



def home(request):
    return render(request, 'home.html')

# Create your views here.
def create_task(request):
    if request.method == 'POST':
        name: str = request.POST.get('task-name', '')
        description: str = request.POST.get('task-description', '').strip()
        status_id: Status = Status.objects.get(name='Pendiente')

        deadline_str: str = request.POST.get('task-deadline', '').strip()
        deadline: datetime.datetime = None

        if deadline_str:
            try:
                deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d')

            except ValueError:
                pass

        Task.objects.create(
            name=name,
            description=description,
            deadline=deadline,
            status_id=status_id,
        )

        messages.success(request, '¡Tarea creada exitosamente!')

        return redirect('list-tasks')

    return render(request, 'create_task.html')

def list_tasks(request):
    return render(request, 'list_tasks.html', {
        'tasks': Task.objects.all(),
    })

def edit_task(request, task_id):
  if request.method == 'POST':
      task: Task = Task.objects.get(id=task_id)

      task.name = request.POST.get('task-name', '')
      task.description = request.POST.get('task-description', '').strip()
      task.status_id = Status.objects.get(id=int(request.POST.get('task-status', 0)))

      deadline_str: str = request.POST.get('task-deadline', '').strip()
      deadline: datetime.datetime = None

      if deadline_str:
          try:
              deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d')

          except ValueError:
              pass

      task.deadline = deadline
      task.save()

      messages.success(request, '¡Tarea actualizada exitosamente!')

      return redirect('list-tasks')

  return render(request, 'edit_task.html', {
      'task': Task.objects.get(id=task_id),
      'task_statuses': Status.objects.all(),
  })

def delete_task(request, task_id):
  Task.objects.get(id=task_id).delete()

  messages.success(request, '¡Tarea eliminada exitosamente!')

  return redirect('list-tasks')



from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("list-tasks")  # Redirige a la lista de tareas
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, "¡Registro exitoso!")
            return redirect("list-tasks")

    return render(request, "auth/register.html")

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect, render

def send_email_view(request):
    if request.method == "POST":
        subject = "Asunto del correo"
        message = "Este es el contenido del correo."
        recipient = "destinatario@gmail.com"

        send_mail(
            subject,
            message,
            'sgallegos20001911@gmail.com',  # Debe coincidir con EMAIL_HOST_USER
            [recipient],
            fail_silently=False,
        )
        messages.success(request, "¡Correo enviado con éxito!")

    return render(request, "send_email.html")




@permission_required("task.add_task", raise_exception=True)

def user_logout(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect("login")


@login_required
def list_tasks(request):
    tasks = Task.objects.all()
    return render(request, "list_tasks.html", {"tasks": tasks})




def is_role_admin(user):
    return user.groups.filter(name="admin").exists() or user.is_superuser



@login_required
@user_passes_test(is_role_admin)  # Solo admins pueden acceder
def manage_roles(request):
    users = User.objects.all()
    groups = Group.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        group_id = request.POST.get("group_id")
        action = request.POST.get("action")

        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(id=group_id)

            if action == "add":
                user.groups.add(group)
                messages.success(request, f"Se añadió {user.username} al grupo {group.name}.")
            elif action == "remove":
                user.groups.remove(group)
                messages.warning(request, f"Se eliminó {user.username} del grupo {group.name}.")
            else:
                messages.error(request, "Acción no válida.")

        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
        except Group.DoesNotExist:
            messages.error(request, "Grupo no encontrado.")

        return redirect("manage-roles")

    return render(request, "roles/manage_roles.html", {"users": users, "groups": groups})



@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if not request.user.has_perm(f"task.change_task_{task.id}"):
        raise PermissionDenied("No tienes permiso para editar esta tarea.")

    if request.method == 'POST':
        task.name = request.POST.get('task-name', '')
        task.description = request.POST.get('task-description', '').strip()

        deadline_str = request.POST.get('task-deadline', '').strip()
        deadline = None

        if deadline_str:
            try:
                deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d')
            except ValueError:
                pass

        task.deadline = deadline
        task.save()
        messages.success(request, '¡Tarea actualizada exitosamente!')
        return redirect('list-tasks')

    return render(request, 'edit_task.html', {
        'task': task,
        'task_statuses': Status.objects.all(),
    })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if not request.user.has_perm(f"task.delete_task_{task.id}"):
        raise PermissionDenied("No tienes permiso para eliminar esta tarea.")

    task.delete()
    messages.success(request, '¡Tarea eliminada exitosamente!')
    return redirect('list-tasks')


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from .models import Task

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "list_tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = Task.objects.all()
        filtered_tasks = []
        for task in tasks:
            perm_view = f"task.view_task_{task.id}"
            perm_edit = f"task.edit_task_{task.id}"
            perm_delete = f"task.delete_task_{task.id}"
            if self.request.user.has_perm(perm_view):
                task.can_edit = self.request.user.has_perm(perm_edit)
                task.can_delete = self.request.user.has_perm(perm_delete)
                filtered_tasks.append(task)
        return filtered_tasks

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "create_task.html"
    fields = ["name", "description", "status", "deadline"]
    success_url = reverse_lazy("list-tasks")

    def form_valid(self, form):
        messages.success(self.request, "¡Tarea creada exitosamente!")
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "edit_task.html"
    fields = ["name", "description", "status", "deadline"]
    success_url = reverse_lazy("list-tasks")

    def form_valid(self, form):
        messages.success(self.request, "¡Tarea actualizada exitosamente!")
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("list-tasks")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "¡Tarea eliminada exitosamente!")
        return super().delete(request, *args, **kwargs)
