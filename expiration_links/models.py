from django.db import models


class ExpirationLink(models.Model):
    url = models.URLField()
    token = models.UUIDField()
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f'{self.url}'
