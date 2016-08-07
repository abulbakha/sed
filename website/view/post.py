from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from website.models import User
from website.view.account import UserIsAdminMixin, user_is_admin
# model
from website.models import Post


# forms
class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ()


# views
class ListPostView(UserIsAdminMixin, ListView):
    model = Post
    template_name = 'post/list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListPostView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class CreatePostView(UserIsAdminMixin, CreateView):
    form_class = PostForm
    template_name = 'post/edit.html'

    def get_success_url(self):
        return reverse('post-list')

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)
        context['action'] = reverse('post-new')
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class UpdatePostView(UserIsAdminMixin, UpdateView):
    model = Post
    template_name = 'post/edit.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse('post-list')

    def get_context_data(self, **kwargs):
        context = super(UpdatePostView, self).get_context_data(**kwargs)
        context['action'] = reverse('post-edit', kwargs={'pk': self.get_object().id})
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context


class DeletePostView(UserIsAdminMixin, DeleteView):
    model = Post
    template_name = 'post/delete.html'

    def get_success_url(self):
        return reverse('post-list')

    def get_context_data(self, **kwargs):
        context = super(DeletePostView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'administration'
        return context
