# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import ModelForm
from django.http.response import HttpResponseRedirect
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from website.models import User, File, Resolution, Execution, participants_from_doc, createDeletionNotification, \
    createInfoCreationNotification
# model
from website.models import Document
# forms
from website.view.account import user_is_admin
from website.view.file import FileForm
from website.view.resolution import NewResolutionForm


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        exclude = ()


class NewDocumentForm(ModelForm):
    class Meta:
        model = Document
        exclude = ('version', 'creator_id', 'created_date')


# views
class ListDocumentView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'document/list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListDocumentView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'documents'
        return context

    def get_queryset(self):
        super(ListDocumentView, self).get_queryset();
        account = self.request.user
        user = User.objects.get(login=account.username)
        doc_from_this_user = Q(from_id=user.pk)
        doc_to_this_user = Q(to_id=user.pk)
        resolution_from_this_user = Q(resolution__from_id=user.pk)
        resolution_to_this_user = Q(resolution__to_id=user.pk)
        created_by_this_user = Q(creator_id=user.pk)
        queryset = Document.objects \
            .filter(
            created_by_this_user | doc_from_this_user | doc_to_this_user | resolution_from_this_user | resolution_to_this_user)\
            .distinct()
        return queryset


class CreateDocumentView(LoginRequiredMixin, CreateView):
    form_class = NewDocumentForm
    template_name = 'document/new.html'

    def get_success_url(self):
        return reverse('document-edit', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(CreateDocumentView, self).get_context_data(**kwargs)
        context['action'] = reverse('document-new')
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'documents'

        return context

    def form_valid(self, form):
        document = form.save(commit=False)
        account = self.request.user
        user = User.objects.get(login__exact=account.username)

        document.creator_id = user
        document.created_date = now
        document.version = 1
        document.save()

        users = participants_from_doc(document)
        for user in users:
            createInfoCreationNotification(user, unicode('Новый документ <b>%s</b>','utf-8') % (unicode(document.name)))

        self.object = document
        return HttpResponseRedirect(self.get_success_url())


class UpdateDocumentView(LoginRequiredMixin, UpdateView):
    model = Document
    template_name = 'document/card.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse('document-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateDocumentView, self).get_context_data(**kwargs)
        context['action'] = reverse('document-edit', kwargs={'pk': self.get_object().id})
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'documents'

        try:
            execution = Execution.objects.get(doc_id=self.get_object().id)
        except Execution.DoesNotExist:
            execution = None
        context['execution'] = execution

        resolutions = Resolution.objects.filter(doc_id=self.get_object().id)
        context['resolution_list'] = resolutions
        context['resolution_form'] = NewResolutionForm()

        files = File.objects.filter(doc_id=self.get_object().id)
        context['file_list'] = files
        context['form'] = FileForm

        return context


class DeleteDocumentView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'document/delete.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteDocumentView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'documents'

        return context

    def get_success_url(self):
        return reverse('document-list')

    def delete(self, request, *args, **kwargs):
        document = self.get_object()
        users = participants_from_doc(document)
        url = super(DeleteDocumentView, self).delete(request, args, kwargs)
        for user in users:
            createDeletionNotification(user, unicode('Документ <b>%s</b> удален','utf-8') % (unicode(document.name)))
        return url
