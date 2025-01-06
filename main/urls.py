
from django.urls import path

from .views import (
    get_book,
    get_books_list,
    get_books_by_author,
    get_books_by_publication_year,
    get_books_list_as_rating_group
)


urlpatterns = [
    path('books/', get_books_list, name='list-books'),
    path('books/author/<str:author>/', get_books_by_author,
         name='books-by-author'),
    path('books/year/<int:year>/', get_books_by_publication_year, 
         name='books-by-year'),
    path('books/<str:title>/', get_book, name='get-book'),
    path('books-by-rating/', get_books_list_as_rating_group,)
]
