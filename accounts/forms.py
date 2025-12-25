from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email, RegexValidator
from .models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Придумайте уникальное имя",
                "autocomplete": "username",
            }
        ),
        validators=[
            RegexValidator(
                regex="^[\w.@+-]+$",
                message="Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_",
            )
        ],
        help_text="",
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ваш email адрес",
                "autocomplete": "email",
            }
        ),
        validators=[validate_email],
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Создайте надежный пароль",
                "autocomplete": "new-password",
            }
        ),
        help_text="",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Повторите пароль",
                "autocomplete": "new-password",
            }
        ),
        help_text="",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 3:
            raise forms.ValidationError(
                "Имя пользователя должно содержать минимум 3 символа"
            )
        if len(username) > 150:
            raise forms.ValidationError(
                "Имя пользователя не должно превышать 150 символов"
            )
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов")
        if password1.isdigit():
            raise forms.ValidationError("Пароль не должен состоять только из цифр")
        return password1


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите ваше имя пользователя",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите ваш пароль",
                "autocomplete": "current-password",
            }
        )
    )
