from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from website.models import User
from website.view.account import UserIsAdminMixin, user_is_admin
# model
from website.models import Unit


# forms
class UnitForm(ModelForm):
    class Meta:
        model = Unit
        exclude = ()


# views
class ListUnitView(UserIsAdminMixin, ListView):
    model = Unit
    template_name = 'unit/list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListUnitView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class CreateUnitView(UserIsAdminMixin, CreateView):
    form_class = UnitForm
    template_name = 'unit/edit.html'

    def get_success_url(self):
        return reverse('unit-list')

    def get_context_data(self, **kwargs):
        context = super(CreateUnitView, self).get_context_data(**kwargs)
        context['action'] = reverse('unit-new')
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class UpdateUnitView(UserIsAdminMixin, UpdateView):
    model = Unit
    template_name = 'unit/edit.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse('unit-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateUnitView, self).get_context_data(**kwargs)
        context['action'] = reverse('unit-edit', kwargs={'pk': self.get_object().id})
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class DeleteUnitView(UserIsAdminMixin, DeleteView):
    model = Unit
    template_name = 'unit/delete.html'

    def get_success_url(self):
        return reverse('unit-list')

    def get_context_data(self, **kwargs):
        context = super(DeleteUnitView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context
