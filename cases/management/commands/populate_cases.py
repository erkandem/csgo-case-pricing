from argparse import ArgumentParser

from django.core.management import BaseCommand

from cases.cases_data import ALL_CASES
from cases.models import (
    Case,
    CaseItem,
)
from prices.models import get_case_info_with_all_combinations


class Command(BaseCommand):
    help = "insert some data about cases and items into the database"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            'case_name',
        )

    def handle(self, *args, **options):
        case_name = options.pop('case_name')
        if case_name == 'all':
            case_data = ALL_CASES
        else:
            case_data = ALL_CASES[case_name]

        for case_name, case_items in case_data.items():
            case, _ = Case.objects.get_or_create(name=case_name)
            case_items_mod = get_case_info_with_all_combinations(case_items)
            for item_data in case_items_mod:
                case_item, new = CaseItem.objects.get_or_create(
                    **item_data,
                )
                self.stdout.write(('created %s' if new else 'exists %s') % item_data)
                if case not in case_item.case.all():
                    case_item.case.add(case)
                    self.stdout.write(f'connected {case_item} to {case_name}')
                else:
                    self.stdout.write(f'already connected {case_item} to {case_name}')
