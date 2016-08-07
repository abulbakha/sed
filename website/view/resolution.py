# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.forms import forms, SelectDateWidget
from django.forms.fields import DateTimeField
from django.forms.models import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from website.models import User, Document, participants_from_doc, createCreationNotification, createDeletionNotification, \
    createInfoCreationNotification
from website.view.account import UserIsAdminMixin, user_is_admin
# model
from website.models import Resolution


# forms
class NewResolutionForm(ModelForm):
    control_date = DateTimeField(widget=SelectDateWidget(), required=False)
    class Meta:
        model = Resolution
        exclude = ('created_date', 'doc_id',)

class ResolutionForm(ModelForm):
    class Meta:
        model = Resolution
        exclude = ()


# views
class CreateResolutionView(LoginRequiredMixin, CreateView):
    form_class = NewResolutionForm
    template_name = 'resolution/edit.html'

    def get_success_url(self):
        return reverse('document-edit', kwargs={'pk': self.kwargs.get('doc_id')})

    def get_context_data(self, **kwargs):
        context = super(CreateResolutionView, self).get_context_data(**kwargs)
        context['action'] = reverse('resolution-new', kwargs=self.kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'resolutions'
        context['doc_id'] = self.kwargs.get('doc_id')
        return context

    def form_valid(self, form):
        doc_id = self.kwargs.get('doc_id', None)
        doc = get_object_or_404(Document, pk=doc_id)

        resolution = form.save(commit=False)
        resolution.doc_id = doc
        resolution.created_date = now
        resolution.save()

        users = participants_from_doc(doc)
        for user in users:
            createInfoCreationNotification(user, unicode('Резолюция к документу <b>%s</b> создана','utf-8') % (unicode(doc.name)))

        return HttpResponseRedirect(self.get_success_url())


class UpdateResolutionView(LoginRequiredMixin, UpdateView):
    model = Resolution
    template_name = 'resolution/edit.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse('document-edit', kwargs={'pk': self.kwargs.get('doc_id')})

    def get_context_data(self, **kwargs):
        context = super(UpdateResolutionView, self).get_context_data(**kwargs)
        context['action'] = reverse('resolution-edit', kwargs={'pk': self.get_object().id})
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'resolutions'
        return context


class DeleteResolutionView(LoginRequiredMixin, DeleteView):
    model = Resolution
    template_name = 'resolution/delete.html'

    def get_success_url(self):
        return reverse('document-edit', kwargs={'pk': self.kwargs.get('doc_id')})

    def get_context_data(self, **kwargs):
        context = super(DeleteResolutionView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'resolutions'
        return context

    def delete(self, request, *args, **kwargs):
        doc_id = self.kwargs.get('doc_id', None)
        doc = get_object_or_404(Document, pk=doc_id)
        users = participants_from_doc(doc)
        url = super(DeleteResolutionView, self).delete(request, args, kwargs)
        for user in users:
            createDeletionNotification(user, unicode('Резолюция к <b>%s</b> удалена','utf-8') % (unicode(doc.name)))
        return url
