from requests import ConnectionError
from django.core.management.base import BaseCommand

from search.indexing import delete_all


class Command(BaseCommand):
    help = "Deletes the whole Solr search index"

    def handle(self, *args, **kwargs):
        try:
            delete_all()
        except ConnectionError:
            self.stdout.write(self.style.ERROR("Could not connect to the Solr index"))
