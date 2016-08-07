from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import django.contrib.auth.models as auth
from django.views.generic.detail import DetailView
from website.models import User
from website.view.account import UserIsAdminMixin, user_is_admin


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ()


# views
class ListUserView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user/list.html'
    paginate_by = 5
    queryset = User.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super(ListUserView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'users'
        return context


class ContactUserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/contact.html'

    def get_object(self, queryset=None):
        return super(ContactUserView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ContactUserView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'users'
        return context


class CreateUserView(UserIsAdminMixin, CreateView):
    form_class = UserForm
    template_name = 'user/edit.html'

    def get_success_url(self):
        return reverse('user-list')

    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context['action'] = reverse('user-new')
        context['active_menu'] = 'users'
        context['is_admin'] = user_is_admin(self.request.user)

        return context

    def form_valid(self, form):
        url = super(CreateUserView, self).form_valid(form)
        user = self.object
        user.is_active = True
        user.save()
        auth.User.objects.create_user(username=self.object.login, password=self.object.password,
                                      email=self.object.email)
        return url

    def dispatch(self, request, *args, **kwargs):
        return super(CreateUserView, self).dispatch(request, args, kwargs)


class UpdateUserView(UserIsAdminMixin, UpdateView):
    template_name = 'user/edit.html'
    model = User
    fields = ('__all__')

    def get_success_url(self):
        return reverse('user-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateUserView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['action'] = reverse('user-edit', kwargs={'pk': self.get_object().id})
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'users'
        return context

    def form_valid(self, form):
        url = super(UpdateUserView, self).form_valid(form)
        user = self.object
        user.is_active = True
        user.save()

        try:
            account = auth.User.objects.get(username__exact=user.login)
        except auth.User.DoesNotExist:
            pass

        if account:
            new_password = user.password
            account.username = user.login
            account.set_password(new_password)
            account.email = user.email
            account.is_active = True
            account.save()
        return url


class DeleteUserView(UserIsAdminMixin, DeleteView):
    model = User
    template_name = 'user/delete.html'

    def get_success_url(self):
        return reverse('user-list')

    def get_context_data(self, **kwargs):
        context = super(DeleteUserView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'users'
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()

        try:
            account = auth.User.objects.get(username__exact=user.login)
        except auth.User.DoesNotExist:
            pass
        if account:
            account.is_active = False
            account.save()
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        return super(DeleteUserView, self).dispatch(request, args, kwargs)
