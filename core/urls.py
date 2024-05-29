from django.urls import path
from core import views
from django.contrib.auth.decorators import login_required
from .views import home, UserRegistrationView, LoginView, sesionLogout, edit_profile
from .products import product_List, product_create, product_update, product_delete, product_category
from .brands import brand_List, brand_create, brand_update, brand_eliminate
from .suppliers import supplier_List, create_supplier, update_supplier, eliminate_supplier
from .categories import category_list, create_category, update_category, delete_category
 
app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("edit/", edit_profile, name="edit"),
    path("logout/", sesionLogout, name="logout"),
    path("home/", login_required(views.home), name="home"),
    path('products/', login_required(product_List), name='product_list'),
    path('products/create/', login_required(product_create), name='product_create'),
    path('products/update/<int:id>/', login_required(product_update), name='product_update'),
    path('products/delete/<int:id>/', login_required(product_delete), name='product_delete'),
    path("category/", product_category, name="category"),
    path('brands/', login_required(brand_List), name='brand_list'),
    path('brands/create/', login_required(brand_create), name='brand_create'),
    path("brands/update/<int:id>/", login_required(brand_update), name="brands_update"),
    path("brand/delete/<int:id>/", login_required(brand_eliminate), name="brands_delete"),
    path('suppliers/', login_required(supplier_List), name='supplier_list'),
    path("suppliers/create/", login_required(create_supplier), name="create_supplier"),
    path("suppliers/update/<int:id>", login_required(update_supplier), name="update_supplier"),
    path("suppliers/delete/<int:id>", login_required(eliminate_supplier), name="eliminate_supplier"),
    path("categories/", login_required(category_list), name="category_list"),
    path("categories/create/", login_required(create_category), name="create_category"),
    path("categories/update/<int:id>", login_required(update_category), name="update_category"),
    path("categories/delete/<int:id>", login_required(delete_category), name="delete_category"),
]