from datetime import date
from .models import Book


def populate_books():
    sample_books = [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "publication_date": date(1925, 4, 10),
            "available": True,
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "publication_date": date(1960, 7, 11),
            "available": True,
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "publication_date": date(1949, 6, 8),
            "available": False,
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "publication_date": date(1813, 1, 28),
            "available": True,
        },
        {
            "title": "Moby-Dick",
            "author": "Herman Melville",
            "publication_date": date(1851, 10, 18),
            "available": False,
        },
        {
            "title": "War and Peace",
            "author": "Leo Tolstoy",
            "publication_date": date(1869, 1, 1),
            "available": True,
        },
        {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "publication_date": date(1951, 7, 16),
            "available": True,
        },
        {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "publication_date": date(1937, 9, 21),
            "available": True,
        },
        {
            "title": "Brave New World",
            "author": "Aldous Huxley",
            "publication_date": date(1932, 8, 30),
            "available": False,
        },
        {
            "title": "Jane Eyre",
            "author": "Charlotte Brontë",
            "publication_date": date(1847, 10, 16),
            "available": True,
        },
    ]

    books = [Book(**book) for book in sample_books]
    Book.objects.bulk_create(books)
