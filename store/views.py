from django.shortcuts import render, get_object_or_404
from django.utils.translation import activate
from dashboard.models import Product, Department, Category
from dashboard.services import filtering, paging
from django_ratelimit.decorators import ratelimit


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
def index(request):
    """Main Site Page"""
    activate("ar")
    departments = Department.objects.filter(is_deleted=False)
    return render(
        request,
        "index.html",
        {
            "title": "HomePage",
            "departments": departments,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
def products(request, product_id=None, product_slug=None):
    # retrieve only one product
    if product_id:
        product_data = get_object_or_404(Product, pk=product_id)
        product_department = product_data.category.department
        if product_department:
            product_department_categories = product_department.category.all()
        else:
            product_department_categories = Category.objects.filter(department=None)
            similar_products = []

        for category in product_department_categories:
            products = Product.objects.exclude(id=product_data.id).filter(
                category=category
            )
            similar_products.extend(products)

        # converting the list into a queryset
        similar_products = Product.objects.filter(
            id__in=[product.id for product in similar_products]
        )
        page_obj = paging(request, similar_products, list_len=6)

        return render(
            request,
            "products/product.html",
            {
                "title": str(product_data.name),
                "product": product_data,
                "page": page_obj,
            },
        )
    # list all products
    else:
        products_data = Product.objects.all()
        page_obj = paging(request, products_data)
        filter_form = filtering(request, products_data)
        return render(
            request,
            "products/index.html",
            {
                "title": "Products",
                "search_form": filter_form.form,
                "page": page_obj,
            },
        )
