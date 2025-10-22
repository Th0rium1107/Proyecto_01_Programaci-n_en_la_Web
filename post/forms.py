from django import forms
from .models import Post,Comment, InfoContacto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post  
        fields = ['title', 'content', 'category', 'price', 'is_healthy', 
            'is_available', 'image', 'published']  
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'category': 'Categoría',
            'price': 'Precio',
            'is_healthy': '¿Es saludable?',
            'is_available': '¿Está disponible?',
            'image': 'Imagen del producto',
            'published': '¿Publicar ahora?',
        }
        widgets = {
            'title': forms.TextInput(attrs={'id': 'title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'id': 'content', 'rows': 5, 'class': 'form-control'}),
            'category': forms.Select(attrs={'id': 'category', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'id': 'price', 'class': 'form-control', 'step': '0.01'}),
            'is_healthy': forms.CheckboxInput(attrs={'id': 'is_healthy'}),
            'is_available': forms.CheckboxInput(attrs={'id': 'is_available'}),
            'published': forms.CheckboxInput(attrs={'id': 'published'}),
        }


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado. Usa otro.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
    


class ContactoForm(forms.ModelForm):
    class Meta:
        model = InfoContacto
        fields = ['telefono', 'red_social']
        labels = {
            'telefono': 'Número de teléfono',
            'red_social': 'Red social',
        }
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'red_social': forms.TextInput(attrs={'class': 'form-control'}),
        }
