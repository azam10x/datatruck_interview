from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Book
from .serializers import BookSerializer


def get_books_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET request required'}, status=405)

    params = request.GET
    books = Book.objects.filter(available=True).order_by('-rating')
    page = params.get('page', 1)
    page_size = params.get('page_size', settings.DEFAULT_PAGE_SIZE)

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


def get_books_by_author(request, author):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET request required'}, status=405)

    params = request.GET

    books = Book.objects.filter(author__iexact=author, available=True)
    page = params.get('page', 1)
    page_size = params.get('page_size', settings.DEFAULT_PAGE_SIZE)

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


def get_books_by_publication_year(request, year):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET request required'}, status=405)

    params = request.GET

    books = Book.objects.filter(publication_date__year=year, available=True)
    page = params.get('page', 1)
    page_size = params.get('page_size', settings.DEFAULT_PAGE_SIZE)

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


def get_books_list_as_rating_group(request):
    groupped_books = {1: [], 2: [], 3: [], 4: [], 5: []}
    books = Book.objects.filter(rating__gt=0).order_by('-rating')

    for book in books:
        groupped_books[int(book.rating)].append(BookSerializer(book).to_representation())

    sorted_books = sorted(groupped_books.items(), key=lambda x: len(x[1]), reverse=True)
    return JsonResponse(sorted_books, safe=False)
