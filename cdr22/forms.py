# app/forms.py
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserTestForm(forms.ModelForm):
    # Definimos qué modelo usaremos
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí es donde ocurre la magia de Crispy + Tailwind
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Añadimos un botón de submit con estilos de Tailwind
        self.helper.add_input(Submit('submit', 'Save User', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'))

# class OrdenForm(forms.Form):
