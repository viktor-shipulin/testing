from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = "crud/task_list.html"
    context_object_name = "tasks"


class TaskDetailView(DetailView):
    model = Task
    template_name = "crud/task_detail.html"


class TaskCreateView(CreateView):
    model = Task
    fields = ["title", "description", "done"]
    template_name = "crud/task_form.html"
    success_url = reverse_lazy("crud:task_list")


class TaskUpdateView(UpdateView):
    model = Task
    fields = ["title", "description", "done"]
    template_name = "crud/task_form.html"
    success_url = reverse_lazy("crud:task_list")


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "crud/task_confirm_delete.html"
    success_url = reverse_lazy("crud:task_list")
