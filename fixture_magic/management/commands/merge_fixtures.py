try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Merge a series of fixtures and remove duplicates.'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='files', nargs='+', help='One or more fixture.')

    def write_json(self, output):
        try:
            # check our json import supports sorting keys
            json.dumps([1], sort_keys=True)
        except TypeError:
            self.stdout.write(json.dumps(output, indent=4))
        else:
            self.stdout.write(json.dumps(output, sort_keys=True, indent=4))

    def handle(self, *files, **options):
        """
        Load a bunch of json files.  Store the pk/model in a seen dictionary.
        Add all the unseen objects into output.
        """
        output = []
        seen = {}

        for f in files:
            f = open(f)
            data = json.loads(f.read())
            for obj in data:
                key = '%s|%s' % (obj['model'], obj['pk'])
                if key not in seen:
                    seen[key] = 1
                    output.append(obj)

        self.write_json(output)
