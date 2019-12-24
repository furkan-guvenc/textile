from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Kullanıcı adı', max_length=100)
    password = forms.CharField(label='Şifre', max_length=100)
