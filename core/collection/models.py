from django.db import models


class Dataset(models.Model):
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'collection'
