from django.db import models

class Meaurements(models.Model):
    location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    crated = models.DateTimeField(auto_now_add= True)

    def __str__(self) -> str:
        return f"distance from {self.location} to {self.destination} is {self.distance} km"