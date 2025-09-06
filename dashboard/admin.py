from django.contrib import admin
from .models import Department, Category, Product, Media, User

admin.site.register(
    (
        Department,
        Category,
        Product,
        Media,
        User,
    ),
)
