from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import ModelForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from website.models import User
from website.view.account import UserIsAdminMixin, user_is_admin
# model
from website.models import Meeting


# forms
class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        exclude = ()


# views
class ListMeetingView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'meeting/list.html'
    paginate_by = 5

    def get_queryset(self):
        account = self.request.user
        user = User.objects.get(login=account.username)

        if user_is_admin(account):
            return Meeting.objects.all()
        else:
            meeting_creator = Q(creator_id=user.pk)
            meeting_participant = Q(participant_id=user.pk)
            return  Meeting.objects.filter(meeting_creator|meeting_participant)

    def get_context_data(self, **kwargs):
        context = super(ListMeetingView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'meetings'
        return context


class CreateMeetingView(UserIsAdminMixin, CreateView):
    form_class = MeetingForm
    template_name = 'meeting/edit.html'

    def get_success_url(self):
        return reverse('meeting-list')

    def get_context_data(self, **kwargs):
        context = super(CreateMeetingView, self).get_context_data(**kwargs)
        context['action'] = reverse('meeting-new')
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'meetings'
        return context


class UpdateMeetingView(UserIsAdminMixin, UpdateView):
    model = Meeting
    template_name = 'meeting/edit.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse('meeting-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateMeetingView, self).get_context_data(**kwargs)
        context['action'] = reverse('meeting-edit', kwargs={'pk': self.get_object().id})
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'meetings'
        return context


class DeleteMeetingView(UserIsAdminMixin, DeleteView):
    model = Meeting
    template_name = 'meeting/delete.html'

    def get_success_url(self):
        return reverse('meeting-list')

    def get_context_data(self, **kwargs):
        context = super(DeleteMeetingView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'meetings'
        return context
