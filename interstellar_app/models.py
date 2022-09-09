from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


class InterstellarObject(models.Model):
    name = models.CharField('Nazwa', max_length=256)
    type = models.CharField('Typ', max_length=128)
    constellation = models.CharField('Gwiazdozbiór', max_length=256)
    distance = models.CharField('Odległość (ly)', max_length=128)
    apparent_magnitude = models.FloatField('Jasność (mag)')
    size = models.CharField('Rozmiar', max_length=128)
    messier_catalogue = models.CharField('Katalog Messiera', max_length=16, blank=True, null=True)
    description = models.CharField('Opis', max_length=1024, blank=True, null=True)

    def get_class(self):
        return 'InterstellarObject'


class SolarSystemObject(models.Model):
    name = models.CharField('Nazwa', max_length=128)
    radius = models.BigIntegerField('Promień (km)')
    aphelion = models.FloatField('Aphelium (au)')
    perihelion = models.FloatField('Peryhelium (au)')
    orbital_period = models.FloatField('Okres orbitalny (d)')
    orbital_speed = models.FloatField('Prędkość orbitalna (km/s)')
    rotation_period = models.FloatField('Okres obrotu (h)')
    apparent_magnitude = models.FloatField('Jasność (mag)')
    natural_satellites = models.IntegerField('Liczba naturalnych satelitów')

    def get_class(self):
        return 'SolarSystemObject'


class MoonObject(models.Model):
    name = models.CharField('Nazwa', max_length=128)
    diameter = models.BigIntegerField('Średnica (km)')
    apoapsis = models.IntegerField('Apocentrum (km)')
    periapsis = models.IntegerField('Perycentrum (km)')
    orbital_period = models.FloatField('Okres orbitalny (d)')
    orbital_speed = models.FloatField('Prędkość orbitalna (km/s)')
    rotation_period = models.CharField('Okres obrotu (h)', max_length=128)
    apparent_magnitude = models.FloatField('Jasność (mag)')
    satellite_of = models.ForeignKey(SolarSystemObject, on_delete=models.PROTECT)

    def get_class(self):
        return 'MoonObject'


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interstellar = models.ForeignKey(InterstellarObject, on_delete=models.PROTECT, blank=True, null=True)
    solar = models.ForeignKey(SolarSystemObject, on_delete=models.PROTECT, blank=True, null=True)
    moon = models.ForeignKey(MoonObject, on_delete=models.PROTECT, blank=True, null=True)


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interstellar = models.ForeignKey(InterstellarObject, on_delete=models.PROTECT, blank=True, null=True)
    solar = models.ForeignKey(SolarSystemObject, on_delete=models.PROTECT, blank=True, null=True)
    moon = models.ForeignKey(MoonObject, on_delete=models.PROTECT, blank=True, null=True)
