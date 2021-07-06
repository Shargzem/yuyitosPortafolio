from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from datetime import datetime

from core.models import Sale


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
               data = self.get_graph_sales_year_month()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # def get_graph_sales_year_month(self):
    #     data = []
    #     try:
    #         year = datetime.now().year
    #         for m in range(1, 13):
    #             total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
    #             data.append(total)
    #
    #     except:
    #         pass
    #     return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        return context
