from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tipo(models.Model):
    nombre = models.CharField(max_length=200)
    def __str__(self):              # __unicode__ on Python 2
    	return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=200)
    def __str__(self):              # __unicode__ on Python 2
    	return self.nombre

class EquipoDeComputo(models.Model):
    tipo = models.ForeignKey(Tipo)
    user = models.ForeignKey(User,)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado)
    ubicacion = models.CharField(max_length=200)
    def __str__(self):              # __unicode__ on Python 2
    	return self.marca

class Historial(models.Model):
    equipodecomputo = models.ForeignKey(EquipoDeComputo)
    fecha = models.DateTimeField('fecha de publicacion')
    estado = models.PositiveSmallIntegerField('estado')
    def __str__(self):              # __unicode__ on Python 2
    	return self.fecha

class Reparacion(models.Model):
    equipodecomputo = models.ForeignKey(EquipoDeComputo)
    user = models.ForeignKey(User,)
    fecha = models.DateTimeField('fecha de publicacion')
    motivo = models.CharField(max_length=800)
    descipcion = models.CharField(max_length=800)
    def __str__(self):              # __unicode__ on Python 2
    	return self.motivo