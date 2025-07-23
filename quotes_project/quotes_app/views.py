import csv

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from .models import Author, Tag, Quote
from .services.scraper import scrape_quotes



def home(request):
    """Render the main dashboard with author and tag dropdowns."""
    authors = Author.objects.all()
    tags = Tag.objects.all()
    return render(request, 'index.html', {
        'authors': authors,
        'tags': tags,
    })


@csrf_exempt
@require_POST
def scrape(request):
    """Trigger scraping and return newly added quotes, authors, and tags."""
    try:
        new_quotes = scrape_quotes()
        authors = Author.objects.all().values('id', 'name')
        tags = Tag.objects.all().values('id', 'name_tag')

        return JsonResponse({
            'status': 'success',
            'new_quotes': len(new_quotes),
            'quotes': new_quotes,
            'authors': list(authors),
            'tags': list(tags)        })
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)


def quotes_by_author(request, author_id):
    """Display all quotes for a given author."""
    author = get_object_or_404(Author, id=author_id)
    quotes = Quote.objects.filter(author=author).select_related('author').prefetch_related('tags')
    return render(request, 'quotes_list.html', {
        'quotes': quotes,
        'title': f'Quotes by {author.name}'
    })


def quotes_by_tag(request, tag_id):
    """Display all quotes associated with a specific tag."""
    tag = get_object_or_404(Tag, id=tag_id)
    quotes = Quote.objects.filter(tags=tag).select_related('author').prefetch_related('tags')
    return render(request, 'quotes_list.html', {
        'quotes': quotes,
        'title': f'Quotes tagged with "{tag.name_tag}"'
    })


def download(request):
    """Export all quotes, authors, and tags as a downloadable CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="quotes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Quote', 'Author', 'Tags'])

    quotes = Quote.objects.select_related('author').prefetch_related('tags')

    for quote in quotes:
        tag_list = ', '.join(tag.name_tag for tag in quote.tags.all())
        writer.writerow([quote.text, quote.author.name, tag_list])

    return response


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_quotes(request):
    """Delete all quotes from the database."""
    try:
        Quote.objects.all().delete()
        Author.objects.all().delete()
        Tag.objects.all().delete() 
        return JsonResponse({
            'status': 'success', 
            'message': 'All quotes deleted'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)