from django.urls import path

from cases import views

urlpatterns = [
    path(
        'export/',
        views.ExportView.as_view(),
        name='export-view'
    )
]
