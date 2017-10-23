from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'^hotel_registration', views.hotel_registration, name='hotel_registration'),
    url(r'^trav_settings', views.trav_settings, name='trav_settings'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^registration', views.registration, name='registration'),
    url(r'^authorization', views.authorization, name='authorization'),
    url(r'^book_list', views.BookingListView.as_view(), name='book_list'),
    url(r'^$', views.index, name='index')
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

