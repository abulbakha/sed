from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from website.models import User
from website.view.account import UserIsAdminMixin, user_is_admin
# model
from website.models import Room


# forms
class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ()


# views
class ListRoomView(UserIsAdminMixin, ListView):
    model = Room
    template_name = 'room/list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListRoomView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class CreateRoomView(UserIsAdminMixin, CreateView):
    form_class = RoomForm
    template_name = 'room/edit.html'

    def get_success_url(self):
        return reverse('room-list')

    def get_context_data(self, **kwargs):
        context = super(CreateRoomView, self).get_context_data(**kwargs)
        context['action'] = reverse('room-new')
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class UpdateRoomView(UserIsAdminMixin, UpdateView):
    model = Room
    template_name = 'room/edit.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse('room-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateRoomView, self).get_context_data(**kwargs)
        context['action'] = reverse('room-edit', kwargs={'pk': self.get_object().id})
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class DeleteRoomView(UserIsAdminMixin, DeleteView):
    model = Room
    template_name = 'room/delete.html'

    def get_success_url(self):
        return reverse('room-list')

    def get_context_data(self, **kwargs):
        context = super(DeleteRoomView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context
