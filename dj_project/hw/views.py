from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django import forms
from . import models


class BookingList(ListView):
    model = models.Booking
    template_name = 'booking_list.html'


def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        is_val = form.is_valid()
        if is_val:
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                form.add_error('username',['Логин или пароль введены неверно'])
                is_val = False

        if is_val:
            login(request, user)
            return HttpResponseRedirect('/hw')
    else:
        form = AuthorizationForm()

    return render(request, 'authorization.html',{'form':form})


class AuthorizationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин')
    password = forms.CharField(min_length=8,widget=forms.PasswordInput, label='Пароль')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        is_val = form.is_valid()
        if is_val:
            data = form.cleaned_data
            if data['password']!=data['password2']:
                is_val = False
                form.add_error('password2',['Пароли должны совпадать'])
            #for user in models.User.objects:
                #if data['username'] == user.username:
            if models.User.objects.filter(username=data['username']).exists():
                form.add_error('username',['Пользователь с данным логином уже существует'])
                is_val = False
            if models.User.objects.filter(email=data['email']).exists():
                form.add_error('email',['Пользователь с данной электронной почтой уже зарегестрирован'])
                is_val = False
        if is_val:
            user = models.User.objects.create_user(data['username'], data['email'], data['password'])
            trav = models.Traveler()
            trav.user = user
            trav.first_name = data['first_name']
            trav.last_name = data['last_name']
            trav.save()
            return HttpResponseRedirect('/hw/authorization')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html',{'form':form})


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5,label='Логин')
    password = forms.CharField(min_length=8,widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Повторите ввод')
    email = forms.EmailField(label='Email')
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/hw')


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('authorization')
    else:
        return HttpResponseRedirect('book_list')
