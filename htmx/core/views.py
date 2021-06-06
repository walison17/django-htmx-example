from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Song


class OrderOption:
    def __init__(self, field, direction):
        self.field = field
        self.direction = direction

    def __str__(self):
        return self.field if self.direction == 'asc' else f'-{self.field}'


def index(request):
    query = request.GET.get('q')

    order_fields = {'name', 'artist__name', 'release_year'}
    order_field = request.GET.get('order')
    order_field = order_field if order_field in order_fields else 'name'
    order = OrderOption(order_field, request.GET.get('dir', 'asc'))

    songs = (
        Song
        .objects
        .select_related('artist')
        .order_by(str(order))
    )
    if query:
        songs = songs.filter(Q(name__icontains=query) | Q(artist__name__icontains=query))

    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('size', 15)
    paginator = Paginator(songs, page_size)
    ctx = {
        'page_obj': paginator.get_page(page_number),
        'page_range': paginator.get_elided_page_range(page_number),
        'order_option': order
    }
    if request.htmx:
        return render(request, 'core/fragments/table.html', ctx)
    else:
        return render(request, 'core/index.html', ctx)
