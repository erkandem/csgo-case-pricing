from django.views.generic import ListView

from prices.models import (
    CalculationBatch,
    CaseItemPriceApiResult,
)

from .models import CaseItem


class ExportView(ListView):
    model = CaseItem
    template_name = "cases/export_template.html"

    def get_denormalized_with_price(self):
        batch = CalculationBatch.objects.all().order_by('-id').first()
        api_results = CaseItemPriceApiResult.objects.filter(batch__uuid=batch.uuid).select_related()
        denormalized = list(
            {
                'median_price': api_result.median_price,
                'name': api_result.case_item.name,
                'grade': api_result.case_item.grade,
                'exterior': api_result.case_item.exterior,
                'is_stattrack': api_result.case_item.is_stattrack
            }
            for api_result in api_results
        )
        return denormalized

    def get_denormalized_list(self):
        case_items = [
            {
                "name": item.name,
                "grade": item.grade,
                "exterior": item.exterior,
                "is_stattrack": item.is_stattrack,
             }
            for item in self.object_list
         ]
        return case_items

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['case_items'] = self.get_denormalized_list()
        return context
