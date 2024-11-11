from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#Herda métodos e atributos de UserCreationForm

class CriarUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)           #Incluindo email, que é opcional em Django

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user