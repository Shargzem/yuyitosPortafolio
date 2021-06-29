from datetime import datetime
from django.forms import *


from core.models import Category, Product, Client, Sale


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese Descripción',
                    'rows': 3,
                    'cols': 3
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True


    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del Producto',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2 ',
        'style': 'width: 100% '
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


    #con ajax

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'autocomplete': 'off',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    # con selec2
    search = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'autocomplete': 'off',
        'style': 'width: 100%'
    }))

class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'rut': TextInput(
                attrs={
                    'placeholder': 'Ingrese su rut',
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': Select()
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                #'disabled': True ,
                #'readonly': True,
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }