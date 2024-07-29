from requests import ConnectionError
from django.core.management.base import BaseCommand

from archive.models import Resource
from search.indexing import index_resource, delete_all


class Command(BaseCommand):
    help = "Recreates the entire Solr search index for resources"

    def handle(self, *args, **kwargs):
        try:
            delete_all()
            resources = Resource.objects.all()
            for resource in resources:
                index_resource(resource)
        except ConnectionError:
            self.stdout.write(self.style.ERROR("Could not connect to the Solr index"))
