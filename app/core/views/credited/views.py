from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from core.forms import CreditedForm
from core.models import Credited


class CreditedListView(TemplateView):
    template_name = 'credited/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Credited.objects.all():
                    data.append(i.toJSON())

            elif action == 'add':
                cred = Credited()
                cred.date_joined = request.POST['date_joined']
                cred.date_end = request.POST['date_end']
                cred.total = request.POST['total']
                cred.payment = request.POST['payment']
                cred.state = request.POST['state']
                cred.save()

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Fiado de Clientes'
        context['list_url'] = reverse_lazy('erp:credited_list')
        context['entity'] = 'Fiados'
        context['form'] = CreditedForm()
        return context