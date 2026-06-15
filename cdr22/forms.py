from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from cdr22.roles import ROLE_NAMES


class UsuarioCreateForm(forms.Form):
    PASSWORD_MODE_CHOICES = [
        ('manual', 'Definir contraseña ahora'),
        ('email', 'Enviar correo para configurar contraseña'),
    ]

    first_name = forms.CharField(label='Nombre', max_length=150)
    last_name = forms.CharField(label='Apellido', max_length=150, required=False)
    username = forms.CharField(label='Usuario', max_length=150)
    email = forms.EmailField(label='Correo electrónico')
    role = forms.ModelChoiceField(label='Rol', queryset=Group.objects.none())
    password_mode = forms.ChoiceField(label='Modo de contraseña', choices=PASSWORD_MODE_CHOICES)
    password1 = forms.CharField(label='Contraseña', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', required=False, widget=forms.PasswordInput)
    is_active = forms.BooleanField(label='Usuario activo', required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Group.objects.filter(name__in=ROLE_NAMES).order_by('name')

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Ya existe un usuario con este nombre de usuario.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Ya existe un usuario con este correo electrónico.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password_mode = cleaned_data.get('password_mode')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password_mode == 'manual':
            if not password1:
                self.add_error('password1', 'Ingrese una contraseña.')
            if not password2:
                self.add_error('password2', 'Confirme la contraseña.')
            if password1 and password2 and password1 != password2:
                self.add_error('password2', 'Las contraseñas no coinciden.')
            if password1:
                user = User(
                    username=cleaned_data.get('username', ''),
                    email=cleaned_data.get('email', ''),
                    first_name=cleaned_data.get('first_name', ''),
                    last_name=cleaned_data.get('last_name', ''),
                )
                try:
                    validate_password(password1, user=user)
                except ValidationError as error:
                    self.add_error('password1', error)
        elif password_mode == 'email' and not cleaned_data.get('is_active'):
            self.add_error('is_active', 'El usuario debe estar activo para enviar el correo de configuración de contraseña.')

        return cleaned_data
