from django.test import TestCase
import views

class PrediccionTest(TestCase):
    def testVersion1():
        resultado = views.prediccion_v1(24)
        assert len(resultado) == 24

    def testVersion2():
        resultado = views.prediccion_v2(24)
        assert len(resultado) == 24
