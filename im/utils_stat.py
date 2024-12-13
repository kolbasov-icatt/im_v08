from django.db.models import Sum
from django.db import transaction
from django.db.models.functions import Coalesce
from .models import Product, Sale, WorkingDays, Store, ProductStoreStatistics, ProductStatistics
import numpy as np


def get_month_sales_by_location(year: int, month: int) -> dict:
    """
    Get sales for a chosen month aggregated by store location.
    Args:
        year (int): The year of interest.
        month (int): The month of interest (1-12).
    Returns:
        dict: Sales statistics per product and location.
    Example return:
        {'1021': {'kemerovo': 90, 'novosibirsk': 612}, '1000': {}, '1001': {}, '1005': {'kemerovo': 10, 'novosibirsk': 120}, '1006': {}}
    """
    # Fetch all products
    products = Product.objects.all()

    # Fetch sales data grouped by product and store location
    sales_data = (
        Sale.objects.filter(
            sale_date__year=year,
            sale_date__month=month
        )
        .values('product__sku', 'store__location')  # Group by product and location
        .annotate(total_sales=Coalesce(Sum('quantity'), 0))  # Aggregate sales
    )

    # Initialize the sales statistics dictionary
    statistics = {product.sku: {} for product in products}

    # Populate statistics with aggregated sales
    for sale in sales_data:
        product_sku = sale['product__sku']
        location = sale['store__location']
        total_sales = sale['total_sales']

        if product_sku not in statistics:
            statistics[product_sku] = {}
        statistics[product_sku][location] = total_sales

    return statistics

def get_month_sales(year: int, month: int) -> dict:
    """
    Get sales for a chosen month.
    Args:
        year (int): The year of interest.
        month (int): The month of interest (1-12).
    Returns:
        dict: Sales statistics per product and store.
    """
    products = Product.objects.all()
    stores = Store.objects.all()

    # Initialize the sales statistics dictionary
    statistics = {
        product.sku: {store.location: 0 for store in stores} for product in products
    }

    # Query sales data for the given month
    for store in stores:
        for product in products:
            sales_data = (
                Sale.objects.filter(
                    product=product,
                    store=store,
                    sale_date__year=year,
                    sale_date__month=month
                )
                .aggregate(total_sales=Coalesce(Sum('quantity'), 0))  # Aggregate total sales
            )
            # Update the statistics with total sales for the product at the store
            statistics[product.sku][store.name] = sales_data['total_sales']

    return statistics


def calculate_sales_statistics_product(start_date, end_date):
    # Step 1: Get all working days in the chosen period
    working_days = WorkingDays.objects.filter(date__range=(start_date, end_date)).values_list('date', flat=True)
    
    # Step 2: Retrieve all products
    products = Product.objects.all()

    # Step 3: Prepare results for each product
    product_statistics = []

    for product in products:
        # Step 4: Aggregate sales data for the product, grouped by date
        sales_data = (
            Sale.objects.filter(product=product, sale_date__range=(start_date, end_date))
            .values('sale_date')
            .annotate(total_sales=Coalesce(Sum('quantity'), 0))  # Coalesce ensures no NULLs
        )
        
        # Map sales data to a dictionary for easy lookup
        sales_dict = {sale['sale_date']: sale['total_sales'] for sale in sales_data}

        # Step 5: Generate a list of sales, using 0 for missing days
        sales_list = [sales_dict.get(day, 0) for day in working_days]
        
        # Step 6: Calculate mean and standard deviation
        mean_sales = np.mean(sales_list)
        std_sales = np.std(sales_list)

        # Append the results for the product
        product_statistics.append({
            "product": product.sku,
            "mean_sales": mean_sales,
            "std_sales": std_sales,
            "sales_list": sales_list,  # Optional: Include for debugging or further analysis
        })
    
    return product_statistics

def calculate_sales_statistics(start_date, end_date):
    # Step 1: Get all working days in the chosen period
    working_days = WorkingDays.objects.filter(date__range=(start_date, end_date)).values_list('date', flat=True)

    # Step 2: Retrieve all products and stores
    products = Product.objects.all()
    stores = Store.objects.all()

    # Step 3: Prepare results for each product and store
    statistics_to_save = []
    statistics = {product.sku: {
        store.name: {
            'sales_mean':  None,
            'sales_std':   None,
            'sales_list': [],
        } for store in stores
    } for product in products}

    for store in stores:
        for product in products:
            sales_data = (
                Sale.objects.filter(
                    product=product,
                    store=store,
                    sale_date__range=(start_date, end_date)
                )
                .values('sale_date')
                .annotate(total_sales=Coalesce(Sum('quantity'), 0))  # Coalesce ensures no NULLs
            )
            
            # Map sales data to a dictionary for easy lookup
            sales_dict = {sale['sale_date']: sale['total_sales'] for sale in sales_data}

            # Step 5: Generate a list of sales, using 0 for missing days
            sales_list = [sales_dict.get(day, 0) for day in working_days]
            
            # Step 6: Calculate mean and standard deviation
            mean_sales = np.mean(sales_list).item()
            std_sales = np.std(sales_list).item()

            statistics[product.sku][store.name]['sales_mean'] = mean_sales
            statistics[product.sku][store.name]['sales_std']  = std_sales
            statistics[product.sku][store.name]['sales_list'] = sales_list    

            # Prepare object for saving
            statistics_to_save.append(
                ProductStoreStatistics(
                    product=product,
                    store=store,
                    sales_mean=mean_sales,
                    sales_std=std_sales
                )
            ) 

    # Step 7: Bulk create or update ProductStoreStatistics
    with transaction.atomic():
        for stat in statistics_to_save:
            # Update or create ensures idempotency
            ProductStoreStatistics.objects.update_or_create(
                product=stat.product,
                store=stat.store,
                defaults={
                    'sales_mean': stat.sales_mean,
                    'sales_std': stat.sales_std
                }
            )
    return statistics

def calculate_sales_global_statistics(start_date, end_date):
    working_days = WorkingDays.objects.filter(date__range=(start_date, end_date)).values_list('date', flat=True)
    products = Product.objects.all()

    # Step 3: Prepare results for each product and store
    statistics_to_save = []
    statistics = {product.sku: {  
            'sales_mean':  None,
            'sales_std':   None,
            'sales_list': [],
            'S': None,   
    } for product in products}

    for product in products:
        sales_data = (
            Sale.objects.filter(
                product=product,
                sale_date__range=(start_date, end_date)
            )
            .values('sale_date')
            .annotate(total_sales=Coalesce(Sum('quantity'), 0))  # Coalesce ensures no NULLs
        )
        
        # Map sales data to a dictionary for easy lookup
        sales_dict = {sale['sale_date']: sale['total_sales'] for sale in sales_data}

        # Step 5: Generate a list of sales, using 0 for missing days
        sales_list = [sales_dict.get(day, 0) for day in working_days]
        
        # Step 6: Calculate mean and standard deviation
        mean_sales = np.mean(sales_list).item()
        std_sales = np.std(sales_list).item()

        statistics[product.sku]['sales_mean'] = mean_sales
        statistics[product.sku]['sales_std']  = std_sales
        statistics[product.sku]['sales_list'] = sales_list    
        statistics[product.sku]['S'] = mean_sales * product.S_days    

        # Prepare object for saving
        statistics_to_save.append(
            ProductStatistics(
                product=product,
                sales_mean=mean_sales,
                sales_std=std_sales,
                S=statistics[product.sku]['S'],
            )
        ) 

    # Step 7: Bulk create or update ProductStatistics
    with transaction.atomic():
        for stat in statistics_to_save:
            # Update or create ensures idempotency
            ProductStatistics.objects.update_or_create(
                product=stat.product,
                defaults={
                    'sales_mean': stat.sales_mean,
                    'sales_std': stat.sales_std,
                    'S': stat.S,
                }
            )
    return statistics