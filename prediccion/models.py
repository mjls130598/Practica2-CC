from django.db import models
from mongoengine import connect, Document	
from mongoengine.fields import FloatField, DateTimeField
from datetime import datetime

class Datos(Document):
    fecha = DateTimeField(default=datetime.now())
    temperatura = FloatField(default=0.0)
    humedad = FloatField(default=0.0)
