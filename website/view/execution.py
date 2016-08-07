# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView
from website.models import User, Document, createCreationNotification, participants_from_doc, createDeletionNotification
from website.view.account import user_is_admin
# model
from website.models import Execution


# forms
class ExecutionForm(ModelForm):
    class Meta:
        model = Execution
        exclude = ('doc_id', 'created_date', 'creator_id',)


# views
class CreateExecutionView(LoginRequiredMixin, CreateView):
    form_class = ExecutionForm
    template_name = 'execution/edit.html'

    def get_success_url(self):
        return reverse('document-edit', kwargs={'pk': self.kwargs.get('doc_id')})

    def get_context_data(self, **kwargs):
        context = super(CreateExecutionView, self).get_context_data(**kwargs)
        context['action'] = reverse('execution-new', kwargs=self.kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'documents'
        context['doc_id'] = self.kwargs.get('doc_id')
        return context

    def form_valid(self, form):
        doc_id = self.kwargs.get('doc_id', None)
        doc = get_object_or_404(Document, pk=doc_id)

        account = self.request.user
        user = User.objects.get(login=account.username)

        if not doc.is_executed:
            execution = form.save(commit=False)
            execution.doc_id = doc
            execution.created_date = now
            execution.creator_id = user
            execution.save()

            doc.is_executed = True
            doc.save()

            users = participants_from_doc(doc)
            for user in users:
                createCreationNotification(user, unicode('Документ <b>%s</b> исполнен <b>%s</b>', 'utf-8') % (unicode(doc.name),  unicode(execution.creator_id)))

            return HttpResponseRedirect(self.get_success_url())
        else:
            raise ValidationError("Document is already executed")

class DeleteExecutionView(LoginRequiredMixin, DeleteView):
    model = Execution
    template_name = 'execution/delete.html'

    def get_success_url(self):
        return reverse('document-edit', kwargs={'pk': self.kwargs.get('doc_id')})

    def get_context_data(self, **kwargs):
        context = super(DeleteExecutionView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'documents'
        return context

    def delete(self, request, *args, **kwargs):
        execution = self.get_object()
        doc = execution.doc_id
        doc.is_executed = False
        doc.save()

        users = participants_from_doc(doc)
        for user in users:
            createDeletionNotification(user, unicode('<b>%s</b> удалил исполненение <b>%s</b>', 'utf-8') % (unicode(execution.creator_id), unicode(doc.name)))

        return super(DeleteExecutionView, self).delete(request, args, kwargs)

