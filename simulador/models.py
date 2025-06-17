from django.db import models

#Modelo para las solicitudes del credito
class Solicitudes(models.Model):

    #tipos de empleo para hacer el choice
    tipoEmpleo = [
        ('1', 'Relacion de Dependencia'),
        ('2','Independiente')
    ]

    #Campos del modelo
    nombreCompleto = models.CharField(max_length=100)
    edad = models.IntegerField()
    email = models.CharField(max_length=320)
    celular = models.CharField(max_length=25)
    tipoEmpleo = models.CharField(max_length=1, choices=tipoEmpleo)
    antiguedadLaboral = models.IntegerField()
    ingresoBrutoMensual = models.IntegerField()
    valorPropiedad = models.IntegerField()
    ahorrosDisponibles = models.IntegerField()
    plazoFinanciamiento = models.IntegerField()
    montoCredito = models.FloatField()
    montoCuota = models.FloatField()

    #Asigno para que tenga este nombre en la DB
    class Meta:
        db_table = 'creditos'

#Modelo para las consultas en contactos
class Consultas(models.Model):

    #Campos del modelo
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=320)
    celular = models.CharField(max_length=25)
    mensaje = models.TextField()

    #Asigno para que tenga este nombre en la DB
    class Meta:
        db_table = 'consultas'