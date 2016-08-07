from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import ModelForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

# model
from website.models import Notification, User

# forms
from website.view.account import UserIsAdminMixin


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        exclude = ()

# views
class ListNotificationView(LoginRequiredMixin, ListView):

    model = Notification
    template_name = 'notification/list.html'
    paginate_by = 5

    def get_queryset(self):
        account = self.request.user
        user = User.objects.get(login=account.username)
        for_this_user = Q(user_id=user.pk)
        return Notification.objects.filter(for_this_user)


class CheckNotificationForm(ModelForm):
    class Meta:
        model = Notification
        exclude = ('date','description','type','check','user_id')

class CheckNotificationView(LoginRequiredMixin, UpdateView):

    model = Notification
    template_name = 'notification/delete.html'
    fields = ()

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        n = self.get_object()
        n.check = True
        n.save()
        return HttpResponseRedirect(self.get_success_url())
