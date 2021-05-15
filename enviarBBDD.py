from mongoengine import connect, Document	
from mongoengine.fields import FloatField, DateTimeField
from datetime import datetime
import pandas as pd

connect('practica2', host='mongo')

class Datos(Document):
    fecha = DateTimeField(default=datetime.now())
    temperatura = FloatField(default=0.0)
    humedad = FloatField(default=0.0)

datos = pd.read_csv("./datos.csv")

for index, row in datos.iterrows():
    temperatura = 0 if row["temperature"].isnan() else row["temperature"]
    humedad = 0 if row["humedad"].isnan() else row["humidity"]
    datos = Datos(fecha=row["datetime"], temperatura=temperatura, humedad=temperatura)
    datos.save()
