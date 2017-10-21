from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^registration', views.registration, name='registration'),
    url(r'^authorization', views.authorization, name='authorization'),
    url(r'^book_list', views.BookingList.as_view(), name='book_list'),
    url(r'^$', views.index, name='index')
]
