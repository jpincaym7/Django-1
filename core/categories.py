from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category
from .forms import CategorieForm
from django.contrib import messages

def category_list(request):
    data = {
        "title1": "Categorias",
        "title2": "Consulta de Categorias"
    }
    categories = Category.objects.all()
    data["categories"] = categories
    return render(request, "core/categories/list.html", data)

def create_category(request):
    data = {
        "title1": "Categorias",
        "title2": "Cadastro de Categorias"
        }
    if request.method == "POST":
        form = CategorieForm(request.POST)
        if form.is_valid():
           categorie = form.save(commit=False)
           categorie.user = request.user
           categorie.save()
           messages.success(request, ('LA CATEGORIA SE HA CREADO CON EXITO'))
           return redirect("core:category_list")
        else:
            messages.error(request, "NO ES POSIBLE CREAR LA CATEGORIA")
    else:
        form = CategorieForm()
    data["form"] = form
    return render(request,"core/categories/form.html",data)

def update_category(request, id):
    data = {
        "title1": "Categorias",
        "title2": "Actualización de Categorias"
    }
    categorie = Category.objects.get(pk=id)
    if request.method == "POST":
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, ('LA CATEGORIA SE HA ACTUALIZADO CON EXITO'))
            return redirect("core:category_list")
    else:
        form = CategorieForm(instance=categorie)
        data["form"] = form
        return render(request,"core/categories/form.html", data)
    
def delete_category(request, id):
    data = {
        "title1": "Categorias",
        "title2": "Eliminación de Categorias"
    }
    categorie = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        categorie.delete()
        messages.success(request, ('LA CATEGORIA SE HA ELIMINADO CON EXITO'))
        return redirect("core:category_list")
    data["categorie"] = categorie
    return render(request, "core/categories/delete.html", data)
