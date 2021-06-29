from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.forms import CategoryForm, SupplierForm
from core.models import *




class SupplierListView(ListView):
    model = Supplier
    template_name = 'supplier/list.html'

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
                for i in Supplier.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
        context['create_url'] = reverse_lazy('erp:supplier_create')
        context['list_url'] = reverse_lazy('erp:supplier_list')
        context['entity'] = 'Proveedores'
        # context['object_list'] = Product.objects.all()
        return context


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'supplier/create.html'
    success_url = reverse_lazy('erp:supplier_list')



    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    #     print(request.POST)
    #     form = CategoryForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(self.success_url)
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return render(request, self.template_name, context)


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Proveedores'
        context['entity'] = 'Proveedores'
        context['list_url'] = reverse_lazy('erp:supplier_list')
        # context['object_list'] = Product.objects.all()
        context['action'] = 'add'
        return context



class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'supplier/create.html'
    success_url = reverse_lazy('erp:supplier_list')

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Proveedore'
        context['entity'] = 'Proveedores'
        context['list_url'] = reverse_lazy('erp:supplier_list')
        context['action'] = 'edit'
        return context


class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'supplier/delete.html'
    success_url = reverse_lazy('erp:supplier_list')

    # @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = reverse_lazy('erp:supplier_list')
        return context
