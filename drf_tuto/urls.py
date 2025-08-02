from django.contrib import admin
from django.urls import path, include
from tickets.views import no_rest_no_model, no_rest, guests, guests_fbv, GuestsAPIView, MixinsList, MixinsListPk, GuestListCreateAPIView, GuestRetrieveUpdateDestroyAPIView, GuestsViewSet, MoviesViewSet, ReservationsViewSet, find_movie, add_reservation
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', GuestsViewSet)
router.register('movies', MoviesViewSet)
router.register('reservations', ReservationsViewSet)

urlpatterns = [
    path('', no_rest_no_model, name='no_rest_no_model'),
    path("rest/guests/", guests),
    path("rest/guests/<int:pk>/", guests_fbv),
    path("rest/guests_cbv/", GuestsAPIView.as_view()),
    path("rest/mixins/", MixinsList.as_view()),
    path("rest/mixins/<int:pk>/", MixinsListPk.as_view()),
    path("rest/generics/guests/", GuestListCreateAPIView.as_view()),
    path("rest/generics/guests/<int:pk>/", GuestRetrieveUpdateDestroyAPIView.as_view()),
    path("rest/viewsets/", include(router.urls)),
    path("rest/movies_fbv/movies/", find_movie),
    path("rest/movies/add_reservation/", add_reservation),

    path("guests-all/", no_rest, name='no_rest'),
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin.site.urls),
]
