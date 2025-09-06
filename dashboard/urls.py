from django.urls import path
from .views import (
    # auth
    ulogin,
    register,
    ulogout,
    # user
    get_auth_users,
    get_auth_user,
    activate_user,
    deactivate_user,
    erase_user,
    # main
    index,
    # product
    products,
    add_product,
    edit_product,
    delete_product,
    erase_product,
    # department
    get_departments,
    add_department,
    edit_department,
    delete_department,
    erase_department,
    # offer
    add_offer,
    edit_offer,
    # category
    add_category,
    edit_category,
    erase_category,
    # vistors
    # visitors_analytics,
)

app_name = "dashboard"

urlpatterns = [
    # auth
    path("login/", ulogin, name="login"),
    path("register/", register, name="register"),
    path("logout/", ulogout, name="logout"),
    # user
    path("users/", get_auth_users, name="users"),
    path("activate-user/", activate_user, name="activate-user"),
    path("deactivate-user/", deactivate_user, name="deactivate-user"),
    path("erase-user/", erase_user, name="erase-user"),
    # main
    path("", index, name="index"),
    # Product URLS
    path("products/", products, name="products"),
    path("products/<str:product_id>/<str:product_slug>/", products, name="product"),
    path("add-product/", add_product, name="add-product"),
    path(
        "edit-product/<str:product_id>/<str:product_slug>/",
        edit_product,
        name="edit-product",
    ),
    path("delete-product/<str:product_slug>/", delete_product, name="delete-product"),
    path("delete-product/<str:product_slug>/", delete_product, name="delete-product"),
    path("erase-product/<str:product_slug>/", erase_product, name="erase-product"),
    # Offer URLS
    path("add-offer/<str:product_id>/<str:product_slug>/", add_offer, name="add-offer"),
    path(
        "edit-offer/<str:product_id>/<str:product_slug>/", edit_offer, name="edit-offer"
    ),
    # Departments
    path("departments/", get_departments, name="departments"),
    path("add-department/", add_department, name="add-department"),
    path(
        "edit-department/<str:department_id>/<str:department_slug>/",
        edit_department,
        name="edit-department",
    ),
    path(
        "delete-department/<str:department_slug>/",
        delete_department,
        name="delete-department",
    ),
    path(
        "erase-department/<str:department_slug>/",
        erase_department,
        name="erase-department",
    ),
    # Category URLS
    path("add-category/", add_category, name="add-category"),
    path(
        "edit-category/<str:category_id>/<str:category_slug>/",
        edit_category,
        name="edit-category",
    ),
    path("erase-category/<str:category_slug>/", erase_category, name="erase-category"),
    # Reports
    # path("visitors-analytics/", visitors_analytics, name="visitors-analytics"),
]
