from django.http import Http404
from django.shortcuts import render, redirect
from core.forms import ProductForm
from core.models import Product

def product_List(request):
    data = {
        "title1": "Productos",
        "title2": "Consulta De Productos"
    }
    products = Product.objects.all()
    
    for product in products:
        if not product.image:
            product.image = 'products/default.png'  # Ruta a una imagen por defecto
    
    data["products"] = products
    return render(request, "core/products/list.html", data)


def product_create(request):
    data = {"title1": "Productos", "title2": "Ingreso De Productos"}
   
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Guarda la instancia del producto sin las relaciones many-to-many
            product.user = request.user
            product.save()  # Guarda la instancia del producto
            form.save_m2m()  # Guarda las relaciones many-to-many
            return redirect("core:product_list")
    else:
        form = ProductForm()
    
    data["form"] = form
    return render(request, "core/products/form.html", data)

def product_update(request, id):
    data = {"title1": "Productos", "title2": "Edición De Productos"}
    product = Product.objects.get(pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("core:product_list")
    else:
        form = ProductForm(instance=product)
        data["form"] = form
    return render(request, "core/products/form.html", data)

def product_delete(request, id):
    product = Product.objects.get(pk=id)
    data = {"title1": "Eliminar", "title2": "Eliminar Un Producto", "product": product}
    if request.method == "POST":
        product.delete()
        return redirect("core:product_list")
    return render(request, "core/products/delete.html", data)    

def product_category(request):
    categorie_name = request.GET.get('categorie')
    if not categorie_name:
        raise Http404("Category not specified")
    data = {"title1": "Productos", "title2": "Categorías"}
    products_category = Product.objects.filter(categories=categorie_name)
    data["products_category"] = products_category
    return render(request, "core/products/category.html", data)