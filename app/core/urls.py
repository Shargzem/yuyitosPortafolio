from django.urls import path

from core.templates.dashboard.views import DashboardView
from core.views.category.views import *
from core.views.client.views import ClientView
from core.views.product.views import *
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

    # test
    path('test/', TestView.as_view(), name='test'),

]