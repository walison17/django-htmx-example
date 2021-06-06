from django.contrib import admin

from .models import Artist, Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_year')
    search_fields = ('name',)
    list_filter = ('artist',)
    list_select_related = ('artist',)


admin.site.register(Artist)
