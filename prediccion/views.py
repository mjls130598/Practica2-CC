from django.http import JsonResponse
from prediccion import models
import pandas as pd
import pmdarima as pm
from datetime import datetime, timedelta
from sklearn.linear_model import Ridge
from skforecast.ForecasterAutoreg import ForecasterAutoreg

df = pd.DataFrame(list(models.Datos.objects.values_list('fecha', 'temperatura', 'humedad')),
    columns=['fecha', 'temperatura', 'humedad'])
model_humidityv1 = pm.auto_arima(df["humedad"], start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)

model_temperaturev1 = pm.auto_arima(df["temperatura"], start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)

model_humidityv2 = ForecasterAutoreg(
                regressor = Ridge(normalize=True),
                lags      = 24
             ).fit(df["humedad"])

model_temperaturev2 = ForecasterAutoreg(
                regressor = Ridge(normalize=True),
                lags      = 24
             ).fit(df["temperatura"])

def prediccion_v1(request, horas):

    # Se predice tanto la humedad y temperatura a esa hora
    fc_humedad, confint_humedad = model_humidityv1.predict(
        n_periods=horas, return_conf_int=True)
    fc_temperatura, confint_temperatura = model_temperaturev1.predict(
        n_periods=horas, return_conf_int=True)

    hora_actual = datetime.now.time()
    datos = []
    for i in range(horas):
        hora_futura = hora_actual + timedelta(hours= i + 1)
        datos.append({
            "hora": hora_futura,
            "temperatura": fc_temperatura[i],
            "humedad": fc_humedad[i]
            })
    
    context = {
        "datos" : datos
    }

    return JsonResponse(context)

    

def prediccion_v2(request, horas):

    # Se predice tanto la humedad y temperatura a esa hora
    fc_humedad = model_humidityv2.predict(steps=horas)
    fc_temperatura = model_temperaturev2.predict(steps=horas)

    hora_actual = datetime.now.time()
    datos = []
    for i in range(horas):
        hora_futura = hora_actual + timedelta(hours= i + 1)
        datos.append({
            "hora": hora_futura,
            "temperatura": fc_temperatura[i],
            "humedad": fc_humedad[i]
            })
    
    context = {
        "datos" : datos
    }

    return JsonResponse(context)

