from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView, DeleteView
from .models import *
from .forms import TaskForm


class HomeView(TemplateView):
    template_name = 'home.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        messages.success(self.request, 'Welcome!! Thank you for signing up!')
        return response


class OwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerObjectMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, 'Sorry, you are not authorized to perform this action.')
        return super().handle_no_permission()


class TaskListView(OwnerQuerysetMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().select_related('owner')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)
        return qs.order_by('-created_at')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Task created!')
        return super().form_valid(form)


class TaskUpdateView(OwnerQuerysetMixin, OwnerObjectMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        messages.success(self.request, 'Task updated!')
        return super().form_valid(form)


class TaskDetailView(OwnerQuerysetMixin, OwnerObjectMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskDeleteView(OwnerQuerysetMixin, OwnerObjectMixin, DeleteView):
    model = Task
    template_name = 'tasks/confirm_delete.html'
    success_url = reverse_lazy("tasks:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Task deleted!')
        return super().delete(request, *args, **kwargs)
