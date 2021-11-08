# enconding: utf-8

from django.conf import settings
from django.db import models


class UserRequestHistory(models.Model):
    """
    Model to store the requests done by each user.
    """
    date = models.DateTimeField()
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Request History"
        verbose_name_plural = "User Requests"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user} requested {self.symbol} at {self.date}. " \
               f"H: {self.high}, L: {self.low}, O: {self.open}, C {self.close}"
