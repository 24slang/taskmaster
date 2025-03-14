from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Данный email уже существует')
        return email

    def clean_username(self):
        """
        Переопределение метода для отображение кастомного сообщения
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Данный username уже существует')
        return username

    def clean_password1(self):
        """
        Валидация password1.
        """
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise ValidationError('Пароль должен содержать не менее 8 символов.')

        if not any(char.isdigit() for char in password1):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру.')

        return password1

    def clean_password2(self):
        """
        Валидация password2.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')

        return password2
