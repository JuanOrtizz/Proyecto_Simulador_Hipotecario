from django import forms
from django.forms import Select

#Formulario para la solicitud del credito
class SolicitudCreditoForm(forms.Form):
    nombreCompleto = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre y Apellido', 'id':'nombreCompleto', 'class': 'input_pequeño'}),
        min_length=2,
        max_length=100
    )

    edad = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Edad', 'id':'edad', 'class': 'input_pequeño'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'id':'email' , 'class': 'input_grande'}),
        max_length=320
    )

    celular = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Celular','id':'celular', 'class': 'input_grande'}),
        max_length=25
    )

    tipoEmpleo = forms.ChoiceField(
        choices=[('', 'Tipo de empleo'), ('1', 'Relacion de dependencia'), ('2', 'Independiente')],
        widget=Select(attrs={'id': 'tipoEmpleo', 'class': 'input_pequeño'})
    )

    antiguedadLaboral = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Antiguedad laboral', 'id': 'antiguedadLaboral', 'class': 'input_pequeño'})
    )

    ingresoBrutoMensual = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Ingreso bruto mensual (en pesos)', 'id': 'ingresoBrutoMensual', 'class': 'input_grande'})
    )

    valorPropiedad = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Valor de la propiedad (en pesos)', 'id': 'valorPropiedad','class': 'input_grande'})
    )

    ahorrosDisponibles = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Ahorros disponibles (en pesos)', 'id': 'ahorrosDisponibles', 'class': 'input_grande'})
    )

    plazoFinanciamiento = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Plazo de financiamiento (en años)', 'id': 'plazoFinanciamiento','class': 'input_grande'})
    )

#Formulario para contacto
class ContactoForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre y Apellido', 'id': 'nombre'}),
        min_length=2,
        max_length=100
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'email'}),
        max_length=320
    )

    celular = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Celular', 'id': 'celular' }),
        max_length=25
    )

    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Coloca tu mensaje aqui...', 'id': 'mensaje'})
    )