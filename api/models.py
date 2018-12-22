from django.db import models

class Panel(models.Model):
    brand = models.CharField(max_length=200)
    serial = models.CharField(max_length=16)
    latitude = models.DecimalField(decimal_places=6, max_digits=9)
    longitude = models.DecimalField(decimal_places=6, max_digits=10)

    def __str__(self):
        return "Brand: {0}, Serial: {1}".format(self.brand, self.serial)

class OneHourElectricity(models.Model):
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE)
    kilo_watt = models.DecimalField(decimal_places=3, max_digits=6)
    date_time = models.DateTimeField()

    def __str__(self):
        return "Hour: {0} - {1} KiloWatt".format(self.date_time, self.kilo_watt)
