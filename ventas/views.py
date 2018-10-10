from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.conf import settings
import pandas as pd
from datetime import datetime

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
    inicio = datetime.strptime(inicioReq, '%d/%m/%Y')
    fin = datetime.strptime(finReq, '%d/%m/%Y')
    odoo = settings.odoo
    model = odoo.read('sale.order',[['state', '=', 'sale'], ['date_order', '>', inicioReq] , ['date_order', '<', finReq]],'name date_order partner_id user_id amount_total state')
    model = sorted(model, key=lambda k: k['date_order'], reverse=False) 
    fecha = []
    total = []
    for obj in model:
        date_obj = datetime.strptime(obj['date_order'], '%Y-%m-%d %H:%M:%S')
        fecha.append(date_obj)
        total.append(obj['amount_total'])
    if len(fecha) == 0:
        contexto = {'total': total, 'fecha': fecha}
        return JsonResponse(contexto)
    data = {'dates': fecha, 'values': total}
    tipoFecha = ''
    if tipo == 'dia':
        tipoFecha = 'D'
    elif tipo == 'mes':
        tipoFecha = 'M'
    else:
        tipoFecha = 'A'
        
    df = pd.DataFrame(data)
    df = df.set_index(['dates'])
    df = df.resample(tipoFecha).sum()    
    fecha = df.index.tolist()
    total = df["values"].tolist()
    context = {
        'total': total,
        'fecha': fecha,
    }
    return JsonResponse(context)

def tb_productos(request):
    odoo = settings.odoo
    model = odoo.read('sale.order.line',[['state', '=', 'sale']],'product_id name currency_id price_total product_uom_qty qty_delivered qty_to_invoice qty_invoiced state')
    template = loader.get_template('ventas/tb_productos.html')
    for obj in model:
        obj['product_id'] = obj['product_id'][0]
        obj['currency_id'] = obj['currency_id'][1]
    df = pd.DataFrame(model)
    df= df.groupby(['product_id', 'name', 'state', 'currency_id'])[['price_total','product_uom_qty', 'qty_delivered', 'qty_to_invoice', 'qty_invoiced']].sum().reset_index()
    df = df.sort_values('product_uom_qty',ascending=False)
    out = df.to_dict('records')

    context = {
        'out': out
    }
    return HttpResponse(template.render(context, request))