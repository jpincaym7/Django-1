from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from core.models import Supplier
from core.forms import SupplierForm

def supplier_List(request):
    data = {
        "title1": "Proveedores",
        "title2": "Consulta De Proveedores"
    }
    suppliers = Supplier.objects.all()
    data["suppliers"] = suppliers
    return render(request, "core/suppliers/list.html", data)

def create_supplier(request):
    data = {
        "title1": "Proveedores",
        "title2": "Crear Proveedor"
    }
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            supplier.save()
            messages.success(request, "Proveedor creado exitosamente.")
            return redirect("core:supplier_list")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = SupplierForm()
    data["form"] = form
    return render(request, "core/suppliers/form.html", data)

def update_supplier(request, id):
    data = {
        "title1": "Proveedores",
        "title2": "Actualizar Proveedor"
    }
    supplier = Supplier.objects.get(pk=id)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado exitosamente.")
            return redirect("core:supplier_list")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = SupplierForm(instance=supplier)
    data["form"] = form
    return render(request, "core/suppliers/form.html", data)

    
def eliminate_supplier(request, id):
    data = {
        "title1": "Supplier",
        "title2": "Eliminación de Suppliers"
    }
    Suppliers = get_object_or_404(Supplier, pk=id)
    if request.method == "POST":
        Suppliers.delete()
        return redirect("core:supplier_list")
    data["Suppliers"] = Suppliers
    return render(request, "core/suppliers/delete.html", data)
        