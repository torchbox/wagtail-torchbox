from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    sort_order = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort_order']
