from django.db import models
from django.db.models import Avg

def validate_author(value):
    pass


class BookRating(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.book} - {self.rating}"
    
    def save(self, **kwargs):
        instance = super().save(**kwargs)
        rating = BookRating.objects.filter(book=instance.book).aggregate(Avg('rating'))
        instance.book.rating = rating['rating__avg']
        instance.book.save()
        return instance


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, validators=[validate_author])
    publication_date = models.DateField()
    available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title
