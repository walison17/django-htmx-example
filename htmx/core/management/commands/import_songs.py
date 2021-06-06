import argparse
import csv
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction

from htmx.core.models import Song, Artist


class Command(BaseCommand):
    help = 'Importa as músicas a partir de um arquivo csv'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=argparse.FileType('r', encoding='utf-8'))

    @transaction.atomic
    def handle(self, *args, **options):
        with options['filename'] as f:
            reader = csv.reader(f)
            next(reader)

            songs_by_artist = defaultdict(list)
            for song, artist, release_year, *_ in reader:
                try:
                    release_year = int(release_year)
                except ValueError:
                    release_year = None
                artist = artist.strip().capitalize()
                songs_by_artist[artist].append(Song(name=song.capitalize(), release_year=release_year))

        Artist.objects.bulk_create(Artist(name=a) for a in songs_by_artist.keys())
        artists_map = {a.name: a for a in Artist.objects.all()}

        songs_count = 0
        for artist_name, songs in songs_by_artist.items():
            artist = artists_map[artist_name]
            for s in songs:
                s.artist = artist
            songs_count += len(songs)

        Song.objects.bulk_create(s for songs in songs_by_artist.values() for s in songs)

        self.stdout.write(f'{songs_count} músicas de {len(artists_map)} artistas foram importadas.')
