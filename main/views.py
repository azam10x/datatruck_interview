from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Book
from .serializers import BookSerializer


def get_books_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET request required'}, status=405)

    params = request.GET

    filters = {
        'author__icontains': params.get('author'),
        'publication_date__year': params.get('publication_year'),
        'available': True
    }
    filters = {k: v for k, v in filters.items() if v}

    books = Book.objects.filter(**filters).order_by('id')

    page = params.get('page', 1)
    page_size = params.get('page_size', 10)

    try:
        page_size = int(page_size)
    except ValueError:
        return JsonResponse({
            "error": "Invalid page_size parameter"
        }, status=400)

    paginator = Paginator(books, page_size)

    try:
        paginated_books = paginator.page(page)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    serializer = BookSerializer(instance=paginated_books, many=True)
    data = {
        "total_items": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": paginated_books.number,
        "page_size": len(paginated_books.object_list),
        "data": serializer.to_representation(),
    }

    return JsonResponse(data, safe=False)


def get_book(request, title):
    try:
        book = Book.objects.get(title__icontains=title)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    data = BookSerializer(instance=book).to_representation()
    return JsonResponse(data, safe=False)
