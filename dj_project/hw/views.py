from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models
import logging


logger = logging.getLogger('views')


class BookingListView(ListView):
    model = models.Booking
    template_name = 'booking_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        context['traveler'] = models.Traveler.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        try:
            trav = models.Traveler.objects.get(user=self.request.user)
            qs = models.Booking.objects.filter(user=trav)
        except:
            qs = None
        if qs is not None:
            qs = qs.order_by('-start_date')
        return qs


class SelfHotelListView(ListView):
    model = models.Hotel
    template_name = 'self_hotel_list.html'

    def get_context_data(self, **kwargs):
        context = super(SelfHotelListView, self).get_context_data(**kwargs)
        context['traveler'] = models.Traveler.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        try:
            qs = models.Hotel.objects.filter(owner=self.request.user)
            for q in qs:
                if len(q.description)>50:
                    q.description = q.description[:50]+'...'
        except:
            qs = None
        return qs


class HotelListView(ListView):
    model = models.Hotel
    template_name = 'hotel_list.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(HotelListView, self).get_context_data(**kwargs)
        context['traveler'] = models.Traveler.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        qs = super(HotelListView, self).get_queryset()
        if qs is not None:
            for q in qs:
                if len(q.description)>50:
                    q.description = q.description[:50]+'...'
        return qs


@login_required(login_url='authorization')
def hotel_page(request, hotel):
    try:
        hotel = models.Hotel.objects.get(name=hotel)
    except:
        hotel = None

    traveler = models.Traveler.objects.get(user=request.user)
    return render(request, 'hotel_page.html', {'traveler':traveler, 'hotel':hotel})


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
        form = RegistrationForm(request.POST, request.FILES)
        is_val = form.is_valid()

        if is_val:
            data = form.cleaned_data
            if data['password']!=data['password2']:
                is_val = False
                form.add_error('password2',['Пароли должны совпадать'])
            if models.User.objects.filter(username=data['username']).exists():
                form.add_error('username',['Пользователь с данным логином уже существует'])
                is_val = False
            if models.User.objects.filter(email=data['email']).exists():
                form.add_error('email',['Пользователь с данной электронной почтой уже зарегестрирован'])
                is_val = False

        if is_val:
            traveler = form.save(commit=False)
            traveler.user = models.User.objects.create_user(data['username'], data['email'], data['password'])
            traveler.save()

            return HttpResponseRedirect('/hw/authorization')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html',{'form':form})


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(min_length=5,label='Логин')
    password = forms.CharField(min_length=8,widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Повторите ввод')
    email = forms.EmailField(label='Email')
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    photo = forms.FileField(label='Аватар', widget=forms.ClearableFileInput(attrs={'class':'ask-signup-avatar-input'}),required=False)

    class Meta:
        model = models.Traveler
        fields = ('username', 'password', 'password2', 'email', 'last_name', 'first_name', 'photo')

@login_required(login_url='authorization')
def hotel_registration(request):
    if request.method == 'POST':
        form = HotelRegistrationForm(request.POST, request.FILES)
        is_val = form.is_valid()
        print('validation: {}'.format(is_val))
        if is_val:
            data = form.cleaned_data
            if models.Hotel.objects.filter(name=data['name']).exists():
                form.add_error('name',['Отель с таким названием уже зарегестрирован'])
                is_val = False
        if is_val:
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()

            return HttpResponseRedirect('/hw/hotel_list')
    else:
        form = HotelRegistrationForm()

    traveler = models.Traveler.objects.get(user=request.user)
    return render(request, 'hotel_registration.html', {'form':form, 'traveler':traveler})


class HotelRegistrationForm(forms.ModelForm):
    name = forms.CharField(min_length=5, max_length=30, label='Название')
    adress = forms.CharField(min_length=1, max_length=30, label='Адрес')
    description = forms.CharField(min_length=1, max_length=255, label='Описание')
    #photo = forms.FileField(label='Фотография', widget=forms.ClearableFileInput(attrs={'class':'ask-signup-avatar-input'}), required=False)
    photo = forms.FileField(label='Фотография', required=False)

    class Meta:
        model = models.Hotel
        fields = ('name', 'adress', 'description', 'photo')

@login_required(login_url='authorization')
def booking(request,hotel):
    traveler = models.Traveler.objects.get(user=request.user)
    inits = {'user':'{} {}'.format(traveler.last_name,traveler.first_name),
             'hotel':hotel,
             'price':5000}
    if request.method == "POST":
        form = BookingForm(request.POST, initial=inits)
        is_val = form.is_valid()
        if is_val:
            data = form.cleaned_data
            if not str.isnumeric(data['price']):
                form.add_error('price',['Цена указана некоректно'])
                is_val = False
            if data['start_date'] >= data['end_date']:
                form.add_error('end_date',['Введённая дата отбытия предшествует дате прибытия'])
                is_val = False
        if is_val:
            book = models.Booking()
            book.user = traveler
            book.hotel = models.Hotel.objects.get(name=data['hotel'])
            book.price = int(data['price'])
            book.start_date = data['start_date']
            book.end_date = data['end_date']
            book.save()
            return HttpResponseRedirect('/hw')
    else:
        form = BookingForm(initial=inits)

    return render(request, 'booking.html', {'form':form, 'traveler':traveler})


class BookingForm(forms.Form):
    user = forms.CharField(disabled=True,label='Постоялец')
    hotel = forms.CharField(disabled=True, label='Отель')
    price = forms.CharField(disabled=True,label='Стоимость')
    start_date = forms.DateField(widget=forms.SelectDateWidget(), label='Дата прибытия')
    end_date = forms.DateField(widget=forms.SelectDateWidget(), label='Дата отбытия')


@login_required(login_url='authorization')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/hw')


@login_required(login_url='authorization')
def trav_settings(request):
    return HttpResponse("Такой странички пока нет")


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('authorization')
    else:
        return HttpResponseRedirect('book_list/1')
