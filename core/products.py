from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from core.forms import ProductForm
from core.models import Product
from django.contrib import messages

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
            messages.success(request, ('EL PRODUCTO SE HA CREADO CON EXITO'))
            return redirect("core:product_list")
        else:
            messages.error(request, "NO ES POSIBLE CREAR EL PRODUCTO")
    else:
        form = ProductForm()
    
    data["form"] = form
    return render(request, "core/products/form.html", data)


def product_update(request, id):
    data = {"title1": "Productos", "title2": "Edición De Productos"}
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            form.save_m2m()
            messages.success(request, 'EL PRODUCTO SE HA ACTUALIZADO CON ÉXITO')
            return redirect('core:product_list')
        else:
            messages.error(request, 'NO ES POSIBLE ACTUALIZAR EL PRODUCTO')
    else:
        form = ProductForm(instance=product)
    
    data["form"] = form
    return render(request, 'core/products/form.html', data)

def product_delete(request, id):
    product = Product.objects.get(pk=id)
    data = {"title1": "Eliminar", "title2": "Eliminar Un Producto", "product": product}
    if request.method == "POST":
        product.delete()
        messages.success(request, ('EL PRODUCTO SE HA ELIMINADO CON EXITO'))
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