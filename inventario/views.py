from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.conf import settings
import pandas as pd
from datetime import datetime


def index(request):
    odoo = settings.odoo
    template = loader.get_template('inventario/dashboard.html')
    context = {
        'partners': '',
    }
    return HttpResponse(template.render(context, request))

def data(request):  
    tipo = request.GET.get('tipo', None)
    inicioReq = request.GET.get('inicio', None)
    finReq = request.GET.get('fin', None)  
    odoo = settings.odoo
    productos = odoo.read('product.template',[],'id name type list_price product_name  date categ_id  invoice_policy default_code')
    stock = odoo.read('stock.quant',[['company_id.id','=','1']],'id product_id company_id location_id quantity reserved_quantity in_date')
    for obj in stock:
        obj['product_id'] = obj['product_id'][1]
    df = pd.DataFrame(stock)
    list_stock = df['product_id'].tolist()
    list_stock_qty = df['quantity'].tolist()
    list_stock_res_qty = df['reserved_quantity'].tolist()

    dfProd = pd.DataFrame(productos)
    dfProd = dfProd.sort_values('list_price',ascending=False)    
    list_prod = dfProd['name'].tolist()
    list_prod_price = dfProd['list_price'].tolist()

    dfProdCateg = dfProd.groupby(['type'])['list_price'].sum().reset_index()
    list_prod_category = dfProdCateg['type'].tolist()
    list_prod_category_price = dfProdCateg['list_price'].tolist()
    for i in range (len(list_prod_category)):
        if list_prod_category[i] == "consu":
            list_prod_category[i] = "Consumibles"
        elif list_prod_category[i] == "product":
            list_prod_category[i] = "Productos"
        elif list_prod_category[i]== "service":
            list_prod_category[i]= "Servicios"
    context = {
        'list_stock': list_stock,
        'list_stock_qty': list_stock_qty,
        'list_stock_res_qty': list_stock_res_qty,
        'list_prod': list_prod,
        'list_prod_price': list_prod_price,
        'list_prod_category': list_prod_category,
        'list_prod_category_price': list_prod_category_price,
    }
    return JsonResponse(context)
