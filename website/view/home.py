from datetime import datetime, timedelta, time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from website.models import Document, User, Notification, Meeting
from website.view.account import user_is_admin


class HomeView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'home/home.html'
    paginate_by = 5

    def get_queryset(self):
        account = self.request.user
        user = User.objects.get(login=account.username)

        not_executed = Q(is_executed=False)
        doc_from_this_user = Q(from_id=user.pk)
        doc_to_this_user = Q(to_id=user.pk)
        resolution_from_this_user = Q(resolution__from_id=user.pk)
        resolution_to_this_user = Q(resolution__to_id=user.pk)
        created_by_this_user = Q(creator_id=user.pk)
        queryset = Document.objects\
            .filter(not_executed)\
            .filter(created_by_this_user|doc_from_this_user|doc_to_this_user|resolution_from_this_user|resolution_to_this_user)\
            .distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'home'

        account = self.request.user
        user = User.objects.get(login=account.username)

        notifications = Notification.objects.filter(user_id=user.pk).filter(check=False).distinct()[:3]
        context['notification_list'] = notifications

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        qyear = Q(date__year=year)
        qmonth = Q(date__month=month)
        qday = Q(date__day=day)

        meeting_creator = Q(creator_id=user.pk)
        meeting_participant = Q(participant_id=user.pk)
        meetings = Meeting.objects.filter(meeting_creator|meeting_participant).filter(qyear).filter(qmonth).filter(qday).distinct()[:4]
        context['meeting_list'] = meetings

        return context
