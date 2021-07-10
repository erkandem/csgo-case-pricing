from django.contrib import admin

from .models import (
    Case,
    CaseItem,
)


class CaseAdmin(admin.ModelAdmin):
    pass


class CaseItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Case, CaseAdmin)
admin.site.register(CaseItem, CaseItemAdmin)
