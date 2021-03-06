from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.conf import settings
import pandas as pd
from datetime import datetime
import calendar


class IndexView(generic.TemplateView):
    template_name = 'ventas/index.html'

def listar(request):
    odoo = settings.odoo
    model = odoo.read('sale.order',[['state', '=', 'sale']],'name date_order partner_id user_id amount_total state')
    model = sorted(model, key=lambda k: k['amount_total'], reverse=True) 
    template = loader.get_template('ventas/index.html')
    context = {
        'partners': model,
    }
    return HttpResponse(template.render(context, request))

def gr_total(request):
    odoo = settings.odoo
    model = []
    model = odoo.read('sale.order',[['state', '=', 'sale']],'name date_order partner_id user_id amount_total state')
    model = sorted(model, key=lambda k: k['date_order'], reverse=False) 
    template = loader.get_template('ventas/gr_total.html')
    fecha = []
    total = []
    for obj in model:
        fecha.append(obj['date_order'])
        total.append(obj['amount_total'])
    context = {
        'partners': model,
        'total': total,
        'fecha': fecha,
    }
    return HttpResponse(template.render(context, request))

def gr_tiempo(request):
    template = loader.get_template('ventas/gr_tiempo.html')
    context = {  }
    return HttpResponse(template.render(context, request))



def data_fecha(request):
    tipo = request.GET.get('tipo', None)
    inicioReq = request.GET.get('inicio', None)
    finReq = request.GET.get('fin', None)
    tipoFecha = ''
    if tipo == 'dia':
        tipoFecha = 'D'
    elif tipo == 'mes':
        tipoFecha = 'M'
    else:
        tipoFecha = 'A'

    if tipo == 'dia':
        fecha1_inicio = datetime.strptime(inicioReq, '%d/%m/%Y').strftime("%d/%m/%Y")
        fecha1_fin = datetime.strptime(inicioReq, '%d/%m/%Y').strftime("%d/%m/%Y")
        nombre_mes1 = fecha1_inicio
        
        fecha2_inicio = datetime.strptime(finReq, '%d/%m/%Y').strftime("%d/%m/%Y")
        fecha2_fin = datetime.strptime(finReq, '%d/%m/%Y').strftime("%d/%m/%Y")
        nombre_mes2 = fecha2_inicio
    elif tipo == 'mes':
        fecha1_inicio = datetime.strptime(inicioReq, '%d/%m/%Y').replace(day=1).strftime("%d/%m/%Y")
        fecha1_fin = datetime.strptime(inicioReq, '%d/%m/%Y')
        maximo_dia1 = calendar.monthrange(fecha1_fin.year,fecha1_fin.month)[1]
        fecha1_fin = fecha1_fin.replace(day=maximo_dia1).strftime("%d/%m/%Y")
        nombre_mes1 = datetime.strptime(inicioReq, '%d/%m/%Y').replace(day=1).strftime("%m/%Y")
        
        fecha2_inicio = datetime.strptime(finReq, '%d/%m/%Y').replace(day=1).strftime("%d/%m/%Y")
        fecha2_fin = datetime.strptime(finReq, '%d/%m/%Y')
        maximo_dia2 = calendar.monthrange(fecha2_fin.year,fecha2_fin.month)[1]
        fecha2_fin = fecha2_fin.replace(day=maximo_dia2).strftime("%d/%m/%Y")
        nombre_mes2 = datetime.strptime(finReq, '%d/%m/%Y').replace(day=1).strftime("%m/%Y")

    else:
        fecha1_inicio = datetime.strptime(inicioReq, '%d/%m/%Y').replace(day=1,month=1).strftime("%d/%m/%Y")
        fecha1_fin = datetime.strptime(inicioReq, '%d/%m/%Y').replace(day=31,month=12).strftime("%d/%m/%Y")
        nombre_mes1 = datetime.strptime(inicioReq, '%d/%m/%Y').replace(day=1).strftime("%Y")

        fecha2_inicio = datetime.strptime(finReq, '%d/%m/%Y').replace(day=1,month=1).strftime("%d/%m/%Y")
        fecha2_fin = datetime.strptime(finReq, '%d/%m/%Y').replace(day=31,month=12).strftime("%d/%m/%Y")
        nombre_mes2 = datetime.strptime(finReq, '%d/%m/%Y').replace(day=1).strftime("%Y")


    odoo = settings.odoo
    model = odoo.read('sale.order',[['state', '=', 'sale'], ['date_order', '>=', fecha1_inicio] , ['date_order', '<=', fecha1_fin]],'name date_order partner_id user_id amount_total state partner_id')
    model2 = odoo.read('sale.order',[['state', '=', 'sale'], ['date_order', '>=', fecha2_inicio] , ['date_order', '<=', fecha2_fin]],'name date_order partner_id user_id amount_total state partner_id')
    productos = odoo.read('sale.order.line',[['state', '=', 'sale']],'product_id name currency_id price_total product_uom_qty qty_delivered qty_to_invoice qty_invoiced state')

 
    
    
    
    
        
    df = pd.DataFrame(model)
    try:
        ventas_mes1 = df['amount_total'].sum()
    except:
        ventas_mes1 = 0
    
    df2 = pd.DataFrame(model2)
    try:
        ventas_mes2 = df2['amount_total'].sum()
    except:
        ventas_mes2 = 0
    
    print(ventas_mes1)
    print(ventas_mes2)
    

    try:
        dfPartners = pd.DataFrame(model)
        print(dfPartners)
        dfPartners= dfPartners.groupby(['partner_id'])[['amount_total','state']].sum().reset_index()
        dfPartners= dfPartners.sort_values('amount_total',ascending=False)
        print(dfPartners)
        list_partners = dfPartners['partner_id'].tolist()
        list_partners_amount = dfPartners['amount_total'].tolist()
    except:
        list_partners = []
        list_partners_amount = []
    for obj in productos:
        obj['product_id'] = obj['product_id'][0]
        obj['currency_id'] = obj['currency_id'][1]
    dfProd = pd.DataFrame(productos)
    dfProd= dfProd.groupby(['product_id', 'name', 'state', 'currency_id'])[['price_total','product_uom_qty', 'qty_delivered', 'qty_to_invoice', 'qty_invoiced']].sum().reset_index()
    dfProd = dfProd.sort_values('price_total',ascending=False)
    total_cant_prod_vendidos = dfProd['product_uom_qty'].sum()
    out = dfProd.to_dict('records')
    list_prod_cantidad = []
    list_prod_valor= []
    list_prod_nombre= []
    for obj in out:
        list_prod_cantidad.append(obj["product_uom_qty"])
        list_prod_valor.append(obj["price_total"])
        list_prod_nombre.append(obj["name"])
    print([nombre_mes1,nombre_mes2])
    context = {
        'ventas_mes': [ventas_mes1, ventas_mes2],
        'nombre_mes': [nombre_mes1,nombre_mes2],
        'list_prod_cantidad': list_prod_cantidad,
        'list_prod_valor': list_prod_valor,
        'list_prod_nombre': list_prod_nombre,
        'total_cant_prod_vendidos': total_cant_prod_vendidos,
        'total_ventas': ventas_mes1,
        'list_partners':list_partners,
        'list_partners_amount':list_partners_amount,
    }
    return JsonResponse(context)

def tb_productos(request):
    odoo = settings.odoo
    productos = odoo.read('sale.order.line',[['state', '=', 'sale']],'product_id name currency_id price_total product_uom_qty qty_delivered qty_to_invoice qty_invoiced state')
    template = loader.get_template('ventas/tb_productos.html')
    for obj in productos:
        obj['product_id'] = obj['product_id'][0]
        obj['currency_id'] = obj['currency_id'][1]
    dfProd = pd.DataFrame(productos)
    dfProd= dfProd.groupby(['product_id', 'name', 'state', 'currency_id'])[['price_total','product_uom_qty', 'qty_delivered', 'qty_to_invoice', 'qty_invoiced']].sum().reset_index()
    dfProd = dfProd.sort_values('product_uom_qty',ascending=False)
    out = dfProd.to_dict('records')	
    context = {
        'out': out
    }
    return HttpResponse(template.render(context, request))

def dash(request):
    template = loader.get_template('ventas/dashboard.html')
    context = {  }
    return HttpResponse(template.render(context, request))