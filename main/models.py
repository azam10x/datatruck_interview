from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
