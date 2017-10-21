from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django import forms
from . import models


class BookingListView(ListView):
    model = models.Booking
    template_name = 'booking_list.html'

    #def get(self, request, *args, **kwargs):
        #traveler = models.Traveler.objects.get(user=request.user)
        #return render(request, 'booking_list.html', {'traveler':traveler})
        #return render(request, 'booking_list.html')
    #    return object_


    #def get_context_data(self, **kwargs):
    #    context['o']
    #    context['traveler'] = models.Traveler.objects.get(user=request.user)

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        #context['latest_articles'] = Article.objects.all()[:5]
        context['traveler'] = models.Traveler.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        try:
            qs = models.Booking.objects.filter(user=models.Traveler.objects.get(user=self.request.user))#.get()
        except:
            qs = None
        return qs

def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        is_val = form.is_valid()
        if is_val:
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            try:
                models.Traveler.objects.get(user=user)
            except:
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


def hotel_registration(request):
    return HttpResponse("Такой странички пока нет")


def trav_settings(request):
    return HttpResponse("Такой странички пока нет")


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('authorization')
    else:
        return HttpResponseRedirect('book_list')
