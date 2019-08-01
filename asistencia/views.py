from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.conf import settings
import pandas as pd
from datetime import datetime


def index(request):
    odoo = settings.odoo
    employee = odoo.read('hr.employee',[],'id name')
    template = loader.get_template('asistencia/dashboard.html')
    context = {
        'employee': employee,
    }
    return HttpResponse(template.render(context, request))

def data(request):  
    empleado = request.GET.get('empleado', None)
    inicioReq = request.GET.get('inicio', None)
    finReq = request.GET.get('fin', None)  
    odoo = settings.odoo
    print(empleado)
    ventas = odoo.read('sale.order',[['state', '=', 'sale'], ['date_order', '>', inicioReq] , ['date_order', '<', finReq]],'name date_order partner_id user_id amount_total state partner_id')
    for obj in ventas:
        obj['id_user'] = obj['user_id'][0]
        obj['nombre_user'] = obj['user_id'][1]
    dfVentas = pd.DataFrame(ventas)
    dfVentas = dfVentas.groupby(['id_user','nombre_user'])['amount_total'].sum().reset_index()
    dfVentas = dfVentas.sort_values('amount_total',ascending=False)
    ventas_empleado = dfVentas.to_dict('records')
    print(dfVentas.to_dict('records'))
    list_sell_emp = []
    list_sell_emp_name = []
    list_sell_emp_id = []
    for obj in ventas_empleado:
        list_sell_emp.append(obj["amount_total"])
        list_sell_emp_name.append(obj["nombre_user"])
        list_sell_emp_id.append(obj["id_user"])

    empleado_mes = odoo.read('hr.employee',[['name', '=', list_sell_emp_name[0]]],'id resource_id')
    for obj in empleado_mes:
        empleado_mes_resource = obj["resource_id"][0]
    print (empleado_mes)
    print (empleado_mes_resource)

    if empleado == "0":
        asistencia = odoo.read('hr.attendance',[['check_in', '>=', inicioReq] , ['check_in', '<=', finReq]],'id employee_id worked_hours')
    else:
        asistencia = odoo.read('hr.attendance',[['employee_id.id', '=', empleado] ,['check_in', '>=', inicioReq] , ['check_in', '<=', finReq]],'id employee_id worked_hours')
    if len(asistencia) == 0:
        context = {
            'list_employee': [],
            'list_employee_hours': [],
            'list_sell_emp': list_sell_emp,
            'list_sell_emp_name': list_sell_emp_name,
            'month_employee': list_sell_emp_name[0],
            'month_employee_id': list_sell_emp_id[0],
        }
        return JsonResponse(context)
    for obj in asistencia:
        obj['employee_name'] = obj['employee_id'][1]
        obj['employee_id'] = obj['employee_id'][0]
    df = pd.DataFrame(asistencia).groupby(['employee_id', 'employee_name'])['worked_hours'].sum().reset_index().sort_values('worked_hours',ascending=False)    
    list_employee = df['employee_name'].tolist()
    list_employee_hours = df['worked_hours'].tolist()
    print(list_sell_emp_name[0])
    context = {
        'list_employee': list_employee,
        'list_employee_hours': list_employee_hours,
        'list_sell_emp': list_sell_emp,
        'list_sell_emp_name': list_sell_emp_name,
        'month_employee': list_sell_emp_name[0],
        'month_employee_id': empleado_mes_resource,
    }
    return JsonResponse(context)

