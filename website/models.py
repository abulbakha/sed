# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
from django.utils.timezone import now


@python_2_unicode_compatible
class Department(models.Model):
    class Meta():
        db_table = 'departament'

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class Unit(models.Model):
    class Meta():
        db_table = 'unit'

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    class Meta():
        db_table = 'post'

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class Role(models.Model):
    class Meta():
        db_table = 'role'

    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class User(models.Model):
    class Meta():
        db_table = 'user'

    login = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    address = models.CharField(max_length=100)

    department_id = models.ForeignKey(Department, on_delete=models.PROTECT)
    unit_id = models.ForeignKey(Unit, on_delete=models.PROTECT)
    post_id = models.ForeignKey(Post, on_delete=models.PROTECT)
    role_id = models.ForeignKey(Role, on_delete=models.PROTECT)

    def is_admin(self):
        return self.role_id and self.role_id.name == 'Admin'

    def __str__(self):  # __unicode__ on Python 2
        return self.f_name + ' ' + self.l_name


@python_2_unicode_compatible
class Document(models.Model):
    class Meta():
        db_table = "document"

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    creator_id = models.ForeignKey(User, related_name='document_creator')
    created_date = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)
    from_id = models.ForeignKey(User, related_name='document_from')
    to_id = models.ForeignKey(User, related_name='document_to')
    is_executed = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        files = File.objects.filter(doc_id=self.pk)
        for file in files:
            file.delete()
        super(Document, self).delete(*args, **kwargs)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class Change(models.Model):
    class Meta():
        db_table = 'change'

    date_time = models.DateTimeField(auto_now=True)
    doc_id = models.ForeignKey(Document, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class Resolution(models.Model):
    class Meta():
        db_table = 'resolution'

    created_date = models.DateTimeField(auto_now=True)
    from_id = models.ForeignKey(User, related_name='resolution_from')
    to_id = models.ForeignKey(User, related_name='resolution_to')
    comment = models.CharField(max_length=255, blank=True, null=True)
    control_date = models.DateField(blank=True, null=True)
    doc_id = models.ForeignKey(Document, on_delete=models.PROTECT)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class Execution(models.Model):
    class Meta():
        db_table = 'execution'

    created_date = models.DateTimeField(auto_now=True)
    creator_id = models.ForeignKey(User, on_delete=models.PROTECT)
    doc_id = models.ForeignKey(Document, on_delete=models.PROTECT)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class File(models.Model):
    class Meta():
        db_table = 'file'

    name = models.CharField(max_length=50, unique=True)
    doc_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    uploaded_file = models.FileField()

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.uploaded_file.storage, self.uploaded_file.path
        # Delete the model before the file
        super(File, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class Room(models.Model):
    class Meta():
        db_table = 'room'

    name = models.CharField(max_length=20, unique=True, null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class Meeting(models.Model):
    class Meta():
        db_table = 'meeting'

    date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=100)
    creator_id = models.ForeignKey(User, related_name='meeting_creator')
    participant_id = models.ForeignKey(User, related_name='meeting_participant')

    def __str__(self):  # __unicode__ on Python 2
        return self.description


@python_2_unicode_compatible
class Notification(models.Model):
    class Meta():
        db_table = 'notification'

    date = models.DateField(auto_now=True, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.CharField(max_length=100)
    check = models.BooleanField(default=False)
    type = models.CharField(default="default",max_length=20)

    def __str__(self):  # __unicode__ on Python 2
        return self.description

def createMeetingNotification(user, description):
    createNotification("default", user, description)

def createDeletionNotification(user, description):
    createNotification("danger", user, description)

def createCreationNotification(user, description):
    createNotification("success", user, description)

def createInfoCreationNotification(user, description):
    createNotification("info", user, description)

def createNotification(type, user, description):
    n = Notification()
    n.user_id = user
    n.description = description
    n.type = type
    n.check = False
    n.date = now
    n.save()

def participants_from_doc(doc):
    # for creator, to and from (doc)
    users = set()
    users.add(doc.from_id)
    users.add(doc.to_id)
    users.add(doc.creator_id)

    # for all users in resolutions

    for resolution in doc.resolution_set.all():
        users.add(resolution.to_id)
        users.add(resolution.from_id)

    # user from execution
    for execution in doc.execution_set.all():
        users.add(execution.creator_id)
    return users