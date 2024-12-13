from django.urls import path
from . import views
app_name = 'im'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('sales/', views.sales, name='sales'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('simulate-demand/', views.simulate_demand, name='simulate_demand'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('calculate-statistics/',views.calculate_statistics_view, name='calculate_statistics'),
    path('calculate-statistics-form/', views.calculate_statistics_form, name='calculate_statistics_form'),
    path('place-order/', views.place_order_view, name='place_order'),
    path('stores/', views.store_list, name='store_list'),
]

