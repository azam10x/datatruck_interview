from django.test import TestCase
from datetime import date

from django.urls import reverse
from .models import Book
from .serializers import BookSerializer


class BookSerializerTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_date=date(2023, 1, 1),
            available=True,
        )

    def test_to_representation_single(self):
        serializer = BookSerializer(instance=self.book)
        data = serializer.to_representation()

        expected_data = {
            "title": "Test Book",
            "author": "Test Author",
            "publication_date": "2023-01-01",
            "available": True,
        }
        self.assertEqual(data, expected_data)

    def test_to_representation_many(self):
        Book.objects.create(
            title="Another Book",
            author="Another Author",
            publication_date=date(2022, 12, 31),
            available=False,
        )
        serializer = BookSerializer(instance=Book.objects.all(), many=True)
        data = serializer.to_representation()

        expected_data = [
            {
                "title": "Test Book",
                "author": "Test Author",
                "publication_date": "2023-01-01",
                "available": True,
            },
            {
                "title": "Another Book",
                "author": "Another Author",
                "publication_date": "2022-12-31",
                "available": False,
            },
        ]
        self.assertEqual(data, expected_data)

    def test_is_valid_valid_data(self):
        valid_data = {
            "title": "Valid Book",
            "author": "Valid Author",
            "publication_date": "2023-01-01",
            "available": True,
        }
        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, valid_data)

    def test_is_valid_invalid_data(self):
        invalid_data = {
            "title": "Invalid Book",
            "author": "Invalid Author",
            "publication_date": "invalid-date",
            "available": "not-a-boolean",
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("publication_date", serializer.errors)
        self.assertIn("available", serializer.errors)

    def test_is_valid_missing_fields(self):
        missing_fields_data = {"title": "Missing Fields"}
        serializer = BookSerializer(data=missing_fields_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("author", serializer.errors)
        self.assertIn("publication_date", serializer.errors)
        self.assertIn("available", serializer.errors)

    def test_save_create(self):
        valid_data = {
            "title": "New Book",
            "author": "New Author",
            "publication_date": "2023-01-01",
            "available": True,
        }
        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        new_book = serializer.save()

        self.assertIsInstance(new_book, Book)
        self.assertEqual(new_book.title, "New Book")
        self.assertEqual(new_book.author, "New Author")

    def test_save_update(self):
        update_data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "publication_date": "2024-01-01",
            "available": False,
        }
        serializer = BookSerializer(instance=self.book, data=update_data)
        self.assertTrue(serializer.is_valid())
        updated_book = serializer.save()
        updated_book.refresh_from_db()

        self.assertEqual(updated_book.title, "Updated Book")
        self.assertEqual(updated_book.author, "Updated Author")
        self.assertEqual(updated_book.publication_date, date(2024, 1, 1))
        self.assertFalse(updated_book.available)


class BookViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book1 = Book.objects.create(
            title="Book One",
            author="Author A",
            publication_date=date(2021, 1, 1),
            available=True
        )
        cls.book2 = Book.objects.create(
            title="Book Two",
            author="Author B",
            publication_date=date(2022, 6, 15),
            available=False
        )
        cls.book3 = Book.objects.create(
            title="Another Book",
            author="Author A",
            publication_date=date(2021, 5, 20),
            available=True
        )

    def test_get_books_list(self):
        response = self.client.get(reverse('list-books'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 2)

    def test_get_books_list_with_author_filter(self):
        response = self.client.get(reverse('list-books') + '?author=Author A')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['data']), 2)
        for book in data['data']:
            self.assertIn("Author A", book['author'])

    def test_get_books_list_with_pagination(self):
        response = self.client.get(
            reverse('list-books') + '?page=1&page_size=2'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['total_items'], 2)
        self.assertEqual(data['total_pages'], 1)

    def test_get_books_list_invalid_page_size(self):
        response = self.client.get(
            reverse('list-books') + '?page_size=invalid'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['error'], "Invalid page_size parameter"
        )

    def test_get_books_list_nonexistent_page(self):
        response = self.client.get(reverse('list-books') + '?page=10')
        self.assertEqual(response.status_code, 400)
        self.assertIn("no results", response.json()['error'])

    def test_get_book_by_title(self):
        response = self.client.get(reverse('get-book', args=["Book One"]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], "Book One")
        self.assertEqual(data['author'], "Author A")

    def test_get_book_by_title_not_found(self):
        response = self.client.get(
            reverse('get-book', args=["Nonexistent Book"])
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Book not found")

    def test_get_books_list_invalid_method(self):
        response = self.client.post(reverse('list-books'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['error'], "GET request required")
