from django import forms
from django.shortcuts import redirect, render
from django.views import View
from core.models import Product, Brand, Supplier, Category, Profile
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['description','price','stock','brand','categories','line','supplier','expiration_date','image','state']

class BrandForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields=["description", "state"]

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields= ["name", "ruc", "address", "phone", "state"]
        
class CategorieForm(forms.ModelForm):
    class Meta:
        model = Category
        fields= ["description", "state"]

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    imagen = forms.ImageField(label='Imagen de Perfil', required=False)  # Campo para la imagen de perfil

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'imagen']  # Incluir el campo 'imagen' en los campos del formulario

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(
        label='Imagen de Perfil', 
        required=False, 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Correo electrónico'
            }),
        }


    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['image'].initial = self.instance.profile.image

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        if commit:
            user.save()
            if 'image' in self.cleaned_data:
                profile = Profile.objects.get(user=user)
                profile.image = self.cleaned_data['image']
                profile.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
