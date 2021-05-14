from mongoengine import connect, EmbeddedDocument	
from mongoengine.fields import FloatField, DateTimeField
from datetime import datetime
import panda as pd

connect('practica2', host='mongo')

class Datos(EmbeddedDocument):
    fecha = DateTimeField(default=datetime.datetime.now)
    temperatura = FloatField(default=0.0)
    humedad = FloatField(default=0.0)

datos = pd.read_csv("./datos.csv")

for index, row in datos.iterrows():
    Datos(fecha=row["datatime"], temperatura=row["temperature"], humedad=row["humidity"]).save()

for dato in Datos.objects.all():
    print(dato.fecha)