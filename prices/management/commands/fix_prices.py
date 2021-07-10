from argparse import ArgumentParser

from django.core.management import BaseCommand

from prices.tasks import fix_db_prices


class Command(BaseCommand):
    """

    Example:
        python manage.py \
            operation_broken_fang_case
            bd9331d5-4364-4002-9c91-11483d3d8f65
    """
    help = "Calculate the missing prices of a case from similar items. To be called once after ``calculate_case``"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            'case_name',
        )
        parser.add_argument(
            'batch_uuid',
        )

    def handle(self, *args, **options):
        batch_uuid = options.pop('batch_uuid')
        case_name = options.pop('case_name')
        fix_db_prices(
            batch_uuid,
            case_name,
        )
