"""
Модуль формы поиска
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder

class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                'Регистрация',
                'username',
                'email',
                'password1',
                'password2',
            ),
            ButtonHolder(
                Submit('submit', 'Зарегистрироваться', css_class='btn btn-primary')
            )
        )
