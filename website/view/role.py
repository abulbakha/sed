from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from website.models import User
from website.view.account import UserIsAdminMixin, user_is_admin
# model
from website.models import Role


# forms
class RoleForm(ModelForm):
    class Meta:
        model = Role
        exclude = ()


# views
class ListRoleView(UserIsAdminMixin, ListView):
    model = Role
    template_name = 'role/list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListRoleView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class CreateRoleView(UserPassesTestMixin, CreateView):
    form_class = RoleForm
    template_name = 'role/edit.html'

    def get_success_url(self):
        return reverse('role-list')

    def get_context_data(self, **kwargs):
        context = super(CreateRoleView, self).get_context_data(**kwargs)
        context['action'] = reverse('role-new')
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context

    def test_func(self):
        return False


class UpdateRoleView(UserPassesTestMixin, UpdateView):
    model = Role
    template_name = 'role/edit.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse('role-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateRoleView, self).get_context_data(**kwargs)
        context['action'] = reverse('role-edit', kwargs={'pk': self.get_object().id})
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context

    def test_func(self):
        return False


class DeleteRoleView(UserPassesTestMixin, DeleteView):
    model = Role
    template_name = 'role/delete.html'

    def get_success_url(self):
        return reverse('role-list')

    def get_context_data(self, **kwargs):
        context = super(DeleteRoleView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context

    def test_func(self):
        return False
