from django.urls import path

from core.templates.dashboard.views import DashboardView
from core.views.category.views import *
from core.views.client.views import ClientView
from core.views.credited.views import  CreditedListView
from core.views.product.views import *
from core.views.sale.views import SaleCreateView, SaleListView, SaleDeleteView, SaleUpdateView, SaleInvoicePdfView
from core.views.supplier.views import SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView
from core.views.tests.views import TestView

app_name = 'erp'


urlpatterns = [

    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    #home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    # client
    path('client/', ClientView.as_view(), name='client'),
    # credited
    path('credited/list/', CreditedListView.as_view(), name='credited_list'),


    # test
    path('test/', TestView.as_view(), name='test'),

    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),

    # supplier

    path('supplier/list/', SupplierListView.as_view(), name='supplier_list'),
    path('supplier/add/', SupplierCreateView.as_view(), name='supplier_create'),
    path('supplier/update/<int:pk>/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('supplier/delete/<int:pk>/', SupplierDeleteView.as_view(), name='supplier_delete'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),

]