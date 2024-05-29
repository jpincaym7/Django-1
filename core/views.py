from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from core.forms import UserRegistrationForm, LoginForm, EditProfileForm
from core.forms import ProductForm
from core.models import Product, Profile, Brand, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    datas = []
    data = {
            "header":"Home",
    }
    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    data["products"] = products
    data["brands"] = brands
    data["category"] = categories
    return render(request,'core/home.html',data)


class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'core/auth/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            imagen = form.cleaned_data.get('imagen')
            user = User.objects.create_user(username=username, email=email, password=password)
            if imagen:
                profile = Profile.objects.create(user=user, image=imagen)
            return redirect('login')  # Redirigir a la página de inicio de sesión
        return render(request, 'core/auth/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'core/auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
        return render(request, 'core/auth/login.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('core:home')
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'core/auth/edit_profile.html', {'form': form})


def sesionLogout(request):
    logout(request)
    return redirect('login')