# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_password(value):
    if len(value) != 4 or not value.isdigit():
        raise ValidationError('비밀번호는 숫자 4자리여야 합니다.')
class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    age = forms.IntegerField()
    password1 = forms.CharField(validators=[validate_password])
    password2 = forms.CharField(validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'name', 'age', 'password1', 'password2', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        return password2
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
