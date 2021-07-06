from django.urls import path

from reports.views import ReportSaleView

urlpatterns = [
    path('sale/', ReportSaleView.as_view(), name='sale_report')
]