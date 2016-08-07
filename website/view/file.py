from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from website.models import User, Document
from website.view.account import UserIsAdminMixin, user_is_admin
# model
from website.models import File


# forms
class FileForm(ModelForm):
    class Meta:
        model = File
        exclude = ('doc_id',)


# views
class CreateFileView(LoginRequiredMixin, CreateView):
    form_class = FileForm
    template_name = 'file/edit.html'

    def get_success_url(self):
        return reverse('document-edit', kwargs={'pk': self.kwargs.get('doc_id')})

    def get_context_data(self, **kwargs):
        context = super(CreateFileView, self).get_context_data(**kwargs)
        context['action'] = reverse('file-new', kwargs=self.kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'files'
        return context

    def form_valid(self, form):
        doc_id = self.kwargs.get('doc_id', None)
        doc = get_object_or_404(Document, pk=doc_id)

        uploaded_file = self.request.FILES['uploaded_file']

        file = form.save(commit=False)
        file.doc_id = doc
        # file.uploaded_file = uploaded_file
        file.save()
        return HttpResponseRedirect(self.get_success_url())


class DeleteFileView(LoginRequiredMixin, DeleteView):
    model = File
    template_name = 'file/delete.html'

    def get_success_url(self):
        return reverse('document-edit', kwargs={'pk': self.kwargs.get('doc_id')})

    def get_context_data(self, **kwargs):
        context = super(DeleteFileView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'files'
        return context


class DownloadFileView(LoginRequiredMixin, DeleteView):
    model = File
    template_name = 'file/delete.html'

    def get_success_url(self):
        return reverse('document-edit', kwargs={'pk': self.kwargs.get('doc_id')})

    def get_context_data(self, **kwargs):
        context = super(DeleteFileView, self).get_context_data(**kwargs)
        context['is_admin'] = user_is_admin(self.request.user)
        context['active_menu'] = 'files'
        return context
