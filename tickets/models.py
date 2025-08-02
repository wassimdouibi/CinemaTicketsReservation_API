from django.db import models


class Movie(models.Model):
    hall = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    start_time = models.DateField()


class Guest(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12, blank=True, null=True)


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.SET_DEFAULT, default="Unknown Movie")
    seats = models.PositiveIntegerField(help_text="Number of seats reserved")
    price = models.DecimalField(max_digits=4, decimal_places=2, help_text="Price per seat")
