from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.template import loader

from django.conf import settings
import xmlrpc.client
import erppeek
from operator import itemgetter, attrgetter

class IndexView(generic.TemplateView):
    template_name = 'ventas/index.html'

def listar(request):
    config = getattr(settings, "ODOO_HOST", False)
    try:
        settings.odoo = erppeek.Client("%s:%d" % (config['HOST'], config['PORT']), db=config['DB'],
                                       user=config['USER'], password=config['PASSWORD'], verbose=False)
        settings.odoo.context = {"lang": settings.LANGUAGE_CODE}
        settings.odoo_models = {}
        settings.deferred_m2o = {}
        settings.deferred_o2m = {}
    except ConnectionRefusedError:
        print("Unable to connect to a running Odoo server.")
        raise
    odoo = settings.odoo
    model = odoo.read('sale.order',[['state', '=', 'sale']],'name date_order partner_id user_id amount_total state')
    model = sorted(model, key=lambda k: k['amount_total'], reverse=True) 
    template = loader.get_template('ventas/index.html')
    context = {
        'partners': model,
    }
    return HttpResponse(template.render(context, request))