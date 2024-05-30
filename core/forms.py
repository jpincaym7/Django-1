from django import forms
from django.shortcuts import redirect, render
from django.views import View
from core.models import Product, Brand, Supplier, Category, Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description', 'price', 'stock', 'brand', 'categories', 'line', 'supplier', 'expiration_date', 'image', 'state']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),  # Widget para elegir la fecha
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.is_update = kwargs.get('instance') is not None
        # Si estamos actualizando, establecer los valores iniciales de los campos
        if self.is_update:
            instance = kwargs.get('instance')
            self.fields['description'].initial = instance.description
            self.fields['price'].initial = instance.price
            self.fields['stock'].initial = instance.stock
            self.fields['brand'].initial = instance.brand
            self.fields['categories'].initial = instance.categories.all()  # Para campos ManyToManyField
            self.fields['line'].initial = instance.line
            self.fields['supplier'].initial = instance.supplier
            self.fields['expiration_date'].initial = instance.expiration_date
            self.fields['image'].initial = instance.image
            self.fields['state'].initial = instance.state


    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description')
        if not self.is_update and Product.objects.filter(description=description).exists():
            raise forms.ValidationError("Ya existe un producto con esta descripción.")
        # Agrega aquí tus otras validaciones personalizadas si es necesario
        return cleaned_data

    def save(self, commit=True):
        if not self.is_update:
            # Si no es una actualización, estamos creando un nuevo producto
            return super(ProductForm, self).save(commit=commit)
        # Si es una actualización, simplemente guardamos la instancia actualizada
        return super(ProductForm, self).save(commit=commit)

    
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["description", "state"]

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        self.is_creation = kwargs.get('instance') is None

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if self.is_creation and Brand.objects.filter(description__iexact=description.lower()).exists():
            raise forms.ValidationError("Esta marca ya existe.")
        return description


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "ruc", "address", "phone", "state"]

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.is_creation = kwargs.get('instance') is None

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if self.is_creation and Supplier.objects.filter(ruc=ruc).exists():
            raise forms.ValidationError("Este RUC ya está registrado.")
        return ruc
        
class CategorieForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["description", "state"]

    def __init__(self, *args, **kwargs):
        super(CategorieForm, self).__init__(*args, **kwargs)
        self.is_creation = kwargs.get('instance') is None

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if self.is_creation and Category.objects.filter(description=description).exists():
            raise forms.ValidationError("Esta categoría ya existe.")
        return description


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    imagen = forms.ImageField(label='Imagen de Perfil', required=True)  # Campo para la imagen de perfil

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'imagen']  # Incluir el campo 'imagen' en los campos del formulario

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email ya está registrado.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return username

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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_users = User.objects.exclude(pk=self.instance.pk)  # Exclude current user from queryset
        if existing_users.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado por otro usuario.')
        return email

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        if commit:
            user.save()
            if 'image' in self.cleaned_data:
                profile = Profile.objects.get_or_create(user=user)[0]
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
