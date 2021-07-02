import json

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from core.forms import SaleForm
from core.models import Sale, Product, DetSale


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:dashboard')
    permission_required = 'erp.add_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                data = []
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'add':

                vents =  json.loads(request.POST['vents'])

                sale = Sale()
                sale.date_joined = vents['date_joined']
                sale.cli_id = vents['cli']
                sale.subtotal = int(vents['subtotal'])
                sale.iva = vents['iva']
                sale.total = int(vents['total'])
                sale.save()


                for i in vents['products']:
                    det = DetSale()
                    det.sale_id = sale.id
                    det.prod_id = i['id']
                    det.cant = int(i['cant'])
                    det.price = int(i['price_sale'])
                    det.subtotal = int(i['subtotal'])
                    det.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'add'
        return context