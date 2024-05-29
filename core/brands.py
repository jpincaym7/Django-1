from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.forms import BrandForm
from core.models import Brand

def brand_List(request):
    data = {
        "title1": "Marcas",
        "title2": "Consulta De Marcas De Productos"
    }
    brands = Brand.objects.all()
    data["brands"] = brands
    return render(request, "core/brands/list.html", data)

def brand_create(request):
    data = {"title1": "Crear", "title2": "Crear una marca"}
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.user = request.user
            brand.save()
            return redirect("core:brand_list")
    else:
        form = BrandForm()
    data["form"] = form
    return render(request, "core/brands/form.html", data)

def brand_update(request, id):
    data = {"title1": "Productos", "title2": "Edición De Productos"}
    brand = Brand.objects.get(pk=id)
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            return redirect("core:brand_list")
    else:
        form = BrandForm(instance=brand)
        data["form"] = form
    return render(request, "core/brands/form.html", data)

def brand_eliminate(request, id):
    brand = Brand.objects.get(pk=id)
    data = {"title1": "Productos", "title2": "Edición De Productos", "Marca": brand}
    if request.method == "POST":
        brand.delete()
        return redirect("core:brand_list")
    else:
        return render(request, "core/brands/delete.html", data)