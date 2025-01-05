
from django.urls import path

from .views import get_books_list, get_book


urlpatterns = [
    path('books/', get_books_list, name='list-books'),
    path('books/<str:title>/', get_book, name='get-book'),
]
