from .models import Movie, Guest, Reservation
from rest_framework.serializers import ModelSerializer


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "hall",
            "title",
            "description",
            "duration",
            "start_time"
        ]


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class GuestSerializer(ModelSerializer):
    class Meta:
        model = Guest
        fields = [
            "pk",
            "name",
            "phone",
            "reservation"
        ]

