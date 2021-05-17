from django.urls import path
from . import views

urlpatterns = [
	path('servicio/v1/prediccion/<int:horas>horas/', views.prediccion_v1, name="version1"),
	path('servicio/v2/prediccion/<int:horas>horas/', views.prediccion_v2, name="version2"),
	]