from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext as _
from django_filters.views import FilterView

from .models import Task
from .filters import TaskFilter
from utils import UserRequiredMixin, SuccessMessageMixin


class TasksListView(UserRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks_show.html'
    filterset_class = TaskFilter
    extra_context = {
        'title': _('Tasks'),
        'button': _('Show'),
        'button_create': _('Create task')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.filterset.qs
        return context


class TaskCreateView(UserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'form.html'
    extra_context = {'title': _('Create task'), 'button': _('Create')}
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(UserRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_show.html"
    extra_context = {'title': _('Task view')}


class TaskUpdateView(UserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ('name', 'description', 'executor', 'labels')
    template_name = 'form.html'
    extra_context = {'title': _('Update task'), 'button': _('Update')}
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully updated')


class TaskDeleteView(UserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    extra_context = {'title': _('Delete task'), 'button': _('Yes, delete')}
    template_name = 'form_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request,
                       _("You cannot delete this task because you are not the creator."))
        return redirect(reverse_lazy('tasks'))
