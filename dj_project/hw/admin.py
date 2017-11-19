from django.contrib import admin
from .models import Traveler, Hotel, Booking

# Register your models here.
@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    list_display = ('username','full_name','has_bookings')
    search_fields = ['last_name', 'first_name']

    def full_name(self, obj):
        return "{} {}".format(obj.last_name, obj.first_name)

    def username(self, obj):
        return "{}".format(obj.user.username)

    def has_bookings(self, obj):
        hs = Booking.objects.filter(user=obj)
        return len(hs)>0

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',  'adress', 'description')

    def owner(self, obj):
        return "{}".format(obj.owner.username)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('username', 'hotelname', 'price', 'start_date', 'end_date')

    def username(self, obj):
        return "{}".format(obj.user.user.username)

    def hotelname(self, obj):
        return "{}".format(obj.hotel.name)
