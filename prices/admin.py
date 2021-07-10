from django.contrib import admin

from .models import (
    CalculationBatch,
    CaseItemPriceApiResult,
    CaseItemPriceDetails,
    CasePrice,
)


class CalculationBatchAdmin(admin.ModelAdmin):
    pass


class CasePriceAdmin(admin.ModelAdmin):
    pass


class CaseItemPriceApiResultAdmin(admin.ModelAdmin):
    pass


class CaseItemPriceDetailsAdmin(admin.ModelAdmin):
    pass


admin.site.register(CalculationBatch, CalculationBatchAdmin)
admin.site.register(CasePrice, CasePriceAdmin)
admin.site.register(CaseItemPriceApiResult, CaseItemPriceApiResultAdmin)
admin.site.register(CaseItemPriceDetails, CaseItemPriceDetailsAdmin)
