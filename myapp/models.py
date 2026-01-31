from django.db import models

class Registro(models.Model):
    dt_hora = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    ip = models.GenericIPAddressField()
    foto = models.ImageField(upload_to='fotos/')

    def __str__(self):
        return f"Registro em {self.dt_hora} - {self.ip}"