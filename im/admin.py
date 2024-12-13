from django.contrib import admin
from .models import (
    Store, Product, ProductStoreData, ProductGlobalData, Sale, ProductOrder, Backlog, 
    Demand, Inventory, WorkingDays, ProductStoreStatistics, ProductStatistics, Region,
    )

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_rus')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'lead_time_mean', 'lead_time_std')
    list_filter = ('location',)
    search_fields = ('name', 'location')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'manufacturer', 'category', 'weight', 'volume')
    search_fields = ('sku', 'name')


@admin.register(ProductStoreData)
class ProductStoreDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'inventory_level', 'total_sales', 'average_demand', 'demand_std')
    list_filter = ('store', 'product')
    search_fields = ('product__name', 'store__name')


@admin.register(ProductGlobalData)
class ProductGlobalDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'total_inventory', 'total_sales', 'average_demand', 'demand_std')
    search_fields = ('product__name',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'inventory_level', 'date')
    list_filter = ('store', 'product', 'date')
    search_fields = ('product__name', 'store__name')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'client_type', 'category', 'manager', 'quantity', 'sale_date')
    list_filter = ('store', 'product', 'client_type', 'category', 'manager', 'sale_date')
    search_fields = ('product__name', 'store__name', 'client_type', 'category', 'manager')


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'quantity', 'order_date', 'expected_delivery_date')
    list_filter = ('store', 'product', 'order_date')
    search_fields = ('product__name', 'store__name')


@admin.register(Backlog)
class BacklogAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'quantity', 'backlog_date')
    list_filter = ('store', 'product', 'backlog_date')
    search_fields = ('product__name', 'store__name')


@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'quantity', 'demand_date')
    list_filter = ('store', 'product', 'demand_date')
    search_fields = ('product__name', 'store__name')


@admin.register(WorkingDays)
class WorkingDaysAdmin(admin.ModelAdmin):
    list_display = ('date',)
    list_filter = ('date',)
    search_fields = ('date', )


@admin.register(ProductStoreStatistics)
class ProductStoreStatisticsAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'sales_mean', 'sales_std', 'S')
    list_filter = ('store', 'product',)
    search_fields = ('product__sku', 'store__name')


@admin.register(ProductStatistics)
class ProductStatisticsAdmin(admin.ModelAdmin):
    list_display = ('product', 'sales_mean', 'sales_std', 'S')
    list_filter = ('product',)
    search_fields = ('product__sku',)

