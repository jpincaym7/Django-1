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
                Profile.objects.create(user=user, image=imagen)
            messages.success(request, 'Usuario registrado exitosamente. Por favor, inicia sesión.')
            return redirect('login')
        else:
            # Revisar errores y mostrar un mensaje general
            general_error_message = "Hubo un error con tu registro. Por favor, revisa el formulario y completa los datos correctamente."
            for field, errors in form.errors.items():
                for error in errors:
                    # Mensajes específicos para contraseñas
                    if 'contraseña' in field:
                        general_error_message = "Las contraseñas no coinciden o no son válidas. Por favor, intenta de nuevo."
                        break
                    # Mensajes específicos para correo y nombre de usuario
                    if 'email' in field or 'username' in field:
                        general_error_message = "El correo electrónico o el nombre de usuario ya están en uso. Por favor, intenta con otros datos."
                        break
                    else:
                        general_error_message = "Todos los campos son obligatorios"
            messages.error(request, general_error_message)
        
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
                messages.success(request, 'INICIO DE SESION EXITOSO.')
                return redirect('core:home')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Formulario inválido. Por favor, revisa los datos proporcionados.')

        return render(request, 'core/auth/login.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'TU PERFIL SE HA ACTUALIZADO CON EXITO.')
            return redirect('core:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
                    # You can customize the messages further if needed
    else:
        form = EditProfileForm(instance=request.user)
    
    # Verificar si el usuario tiene una imagen de perfil, si no, establecer la imagen predeterminada
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if not profile.image:
        profile.image = 'profiles/default.png'
        profile.save()
        messages.info(request, 'No tenías una imagen de perfil. Se ha asignado una imagen predeterminada.')

    return render(request, 'core/auth/edit_profile.html', {'form': form})



def sesionLogout(request):
    logout(request)
    return redirect('login')