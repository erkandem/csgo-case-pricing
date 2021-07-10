from argparse import ArgumentParser

from django.core.management import BaseCommand

from prices.tasks import get_prices_from_api


class Command(BaseCommand):
    """
    Example:
        python manage.py operation_broken_fang_case
    """
    help = "Calculate the current price of a case from it's subcomponents"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            'case_name',
        )

    def handle(self, *args, **options):
        case_name = options.pop('case_name')
        get_prices_from_api(case_name)
