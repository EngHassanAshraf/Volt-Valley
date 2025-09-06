from django.urls import path
from .views import (
    index,
    products,
)

app_name = "mainpages"
urlpatterns = [
    path("", index, name="index"),
    # products
    path("products/", products, name="products"),
    path("products/<str:product_id>/<str:product_slug>/", products, name="product"),
]
