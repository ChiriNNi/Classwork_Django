from django.db import models


class NewModel(models.Model):
    first_field = models.CharField(max_length=100)
    second_field = models.IntegerField()
    third_field = models.DecimalField(max_digits=2, decimal_places=2, default=0.0)

    def __str__(self):
        return self.first_field
