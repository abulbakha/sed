from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import models

from SED import settings
from website.models import User
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django import forms


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['login', 'password']


def UserLogin(request):
    default_page = '/website/'
    if 'next' in request.GET.keys():
        next_page = request.GET['next']
    else:
        next_page = default_page

    if request.user.is_authenticated():
        if next_page != default_page:
            error_msg = "not_enough_permissions"
            return render(request, "account/login.html", {'username': '', 'password': '', 'error_msg': error_msg})
        else:
            return HttpResponseRedirect(next_page)
    else:
        if request.method == 'POST':
            if 'username' in request.POST and 'password' in request.POST:
                username = request.POST['username']
                password = request.POST['password']
                if username and username.strip() and password and password.strip():
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        # Redirect to a success page.
                        login(request, user)
                        return HttpResponseRedirect(next_page)
                    else:
                        # Return a 'disabled account' error message
                        error_msg = 'inactive_user'
                        return render(request, "account/login.html", {'username': username, 'password': password, 'error_msg': error_msg})

            # Return an 'invalid login' error message.
            error_msg = "empty_fields"
            return render(request, "account/login.html", {'username': '', 'password': '', 'error_msg': error_msg})
        else:
            return render(request, "account/login.html", {'username': '', 'password': '', 'next': next_page})


def UserLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def user_is_admin(account):
    username = account.username if account.is_active else ''
    try:
        user = User.objects.get(login=username)
        return user.is_admin()
    except User.DoesNotExist:
        pass
    return False


class UserIsAdminMixin(UserPassesTestMixin):
    """
    A view mixin that only allows admin users to access certain page
    """

    def test_func(self):
        return user_is_admin(self.request.user)
