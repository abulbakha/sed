from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from website.view.account import UserIsAdminMixin, user_is_admin
# model
from website.models import Department


class CreateDepartmentView(UserIsAdminMixin, CreateView):
    model = Department
    template_name = 'department/edit.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse('department-list')

    def get_context_data(self, **kwargs):
        context = super(CreateDepartmentView, self).get_context_data(**kwargs)
        context['action'] = reverse('department-new')
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class ListDepartmentView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'department/list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListDepartmentView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class UpdateDepartmentView(UserIsAdminMixin, UpdateView):
    model = Department
    template_name = 'department/edit.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse('department-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateDepartmentView, self).get_context_data(**kwargs)
        context['action'] = reverse('department-edit', kwargs={'pk': self.get_object().id})
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class DeleteDepartmentView(UserIsAdminMixin, DeleteView):
    model = Department
    template_name = 'department/delete.html'

    def get_success_url(self):
        return reverse('department-list')

    def get_context_data(self, **kwargs):
        context = super(DeleteDepartmentView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context
