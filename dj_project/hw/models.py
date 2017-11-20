from django.db import models
from django.contrib.auth.models import User


class Traveler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    photo = models.ImageField(upload_to='trav_avats/', blank=True, default='trav_avats/default.png', verbose_name='Фотография')

    objects = models.Manager()

    class Meta:
        ordering = ('last_name','first_name',)


class HotelFeature(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')

    objects = models.Manager()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return "{}".format(self.title)


class Hotel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    name = models.CharField(max_length=30, verbose_name='Название')
    adress = models.CharField(max_length=30, verbose_name='Адрес')
    description = models.CharField(max_length=255,null=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='hotel_avats/', blank=True, default='hotel_avats/default.png', verbose_name='Фотография')
    features = models.ManyToManyField(HotelFeature, blank=True, verbose_name='Особенности')

    objects = models.Manager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "{}".format(self.name)


class Booking(models.Model):
    user = models.ForeignKey(Traveler, on_delete=models.CASCADE, verbose_name='Постоялец')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель')
    price = models.IntegerField(verbose_name='Стоимость')
    start_date = models.DateField(verbose_name='Дата заезда')
    end_date = models.DateField(verbose_name='Дата отъезда')

    objects = models.Manager()

    class Meta:
        ordering = ('-start_date',)



