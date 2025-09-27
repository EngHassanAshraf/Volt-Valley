""""""

from django.contrib.auth.models import Group
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import activate
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login, logout
from random import randint
from logging import getLogger

from .models import Product, Media, Department, Category, User
from .forms import (
    RegisterForm,
    ProductForm,
    DepartmentForm,
    CategoryForm,
    MediaForm,
)
from .decorators import is_auth, is_not_auth, is_admin
from .services import filtering, paging, is_logged_in, user_logout

logger = getLogger("dashboard")


# auth
@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_not_auth
def ulogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request=request, username=email, password=password)
        if user:
            if is_logged_in(user)[0]:
                return redirect("store:index")
            login(request, user)
            logger.info(f"user {user.email} logged in")
            return redirect("dashboard:index")
        else:
            logger.warning(f"someone with {email} try to logged in")
            messages.warning(request, "حدث خطأ ما")
            return redirect("store:index")

    return render(
        request,
        "market_admin/ulogin.html",
        {
            "title": "Login",
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = new_user.email.split("@")[0] + str(randint(1000, 9999))
            new_user.save()
            new_user.groups.add(Group.objects.get(name="market_staff"))
            logger.info(
                f"{request.user.email} create a new user with email {new_user.email}"
            )
            return redirect("dashboard:index")
    form = RegisterForm()
    return render(
        request,
        "market_admin/register.html",
        {
            "title": "Creating Admin",
            "form": form,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
def ulogout(request):
    if request.user.is_authenticated:
        logger.info(f"{request.user.email} logged out")
        logout(request)
    return redirect("store:index")


# user


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@is_auth
@is_admin
def get_auth_users(request):
    system_users = User.objects.exclude(id=request.user.id)
    users = {}
    if len(system_users) >= 1:
        users = {
            system_user: is_logged_in(system_user)[0] for system_user in system_users
        }
    return render(
        request,
        "market_admin/users.html",
        {
            "title": "Admins",
            "users": users,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@is_auth
@is_admin
def get_auth_user(request, user_id):

    user = User.objects.get(id=user_id)
    return render(
        request,
        "market_admin/user.html",
        {
            "title": str(user.get_full_name()),
            "users": user,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@is_auth
@is_admin
def deactivate_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        if request.user.id != user_id:
            user = User.objects.get(id=user_id)
            if user.is_active:
                user_logout(user)
                user.is_active = False
                user.save()
                return redirect("dashboard:users")
        else:
            return redirect("dashboard:index")
    else:
        return redirect("store:index")


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@is_auth
@is_admin
def activate_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        user = User.objects.get(id=user_id)
        if user.is_active:
            return redirect("dashboard:index")
        else:
            user.is_active = True
            user.save()
            return redirect("dashboard:users")
    else:
        return redirect("store:index")


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@is_auth
@is_admin
def erase_user(request):
    """Erase Product form the System"""
    if request.method == "POST":
        user_id = request.POST.get("user")
        user = User.objects.get(id=user_id)
        logger.info(f"admin {request.user.email} delete user {user.email}")
        user_logout(user)
        user.delete()
        return redirect("dashboard:users")
    else:
        return redirect("store:index")


# main page


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@is_auth
def index(request):
    """Main Page"""
    return render(
        request,
        "dashboard/index.html",
        {
            "title": "HomePage",
            "categories": Category.objects.all(),
        },
    )


# product


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@is_auth
def products(request, product_id=None, product_slug=None):
    activate("ar")
    if request.method == "GET":
        # retreive product
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            return render(
                request,
                "dashboard/product/product.html",
                {
                    "title": str(product.name),
                    "product": product,
                },
            )
        # list all products
        else:
            products = Product.objects.all()
            filter_form = filtering(request, products)
            page_obj = paging(request, products)

            return render(
                request,
                "dashboard/products.html",
                {
                    "title": "Products",
                    "search_form": filter_form.form,
                    "page": page_obj,
                },
            )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def add_product(request):
    """Create New Product"""
    activate("ar")
    product_form = ProductForm()
    if request.method == "POST":
        new_product = ProductForm(request.POST)
        if new_product.is_valid():
            product_instance = new_product.save()
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "video/mp4"]
            max_size_mb = 2  # Max file size in MB
            max_size_bytes = max_size_mb * 1024 * 1024
            for file in request.FILES.getlist("files"):
                if file.size > max_size_bytes:
                    error_message = f"File size should not exceed {max_size_mb}MB."
                    messages.error(request, str(error_message))
                    product_form = ProductForm(instance=product_instance)
                elif file.content_type not in allowed_types:
                    error_message = (
                        "Invalid file type. Only JPEG, JPG, PNG, and MP4 are allowed."
                    )
                    messages.error(request, error_message)
                    product_form = ProductForm(instance=product_instance)
                else:
                    media_type = (
                        "image" if file.content_type.startswith("image") else "video"
                    )
                    Media.objects.create(
                        product=product_instance, file=file, media_type=media_type
                    ).save()
            logger.info(f"user {request.user.email} add product {product_instance.id}")
            return redirect("dashboard:products")
        else:
            messages.error(request, str(new_product.errors))
            product_form = ProductForm(instance=product_instance)

    return render(
        request,
        "dashboard/product/add_product.html",
        {
            "title": "Adding Product",
            "product_form": product_form,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def edit_product(request, product_id, product_slug):
    """Edit A Product"""
    activate("ar")

    product = Product.objects.get(id=product_id)
    product_medias = Media.objects.filter(product=product)
    media_form_set = modelformset_factory(
        Media,
        form=MediaForm,
        extra=0,
        can_delete=True,
    )

    product_form = ProductForm(instance=product)
    product_medias_forms = media_form_set(queryset=product_medias)

    if request.method == "POST":
        product_new_data = ProductForm(request.POST, instance=product)
        product_medias_data = media_form_set(request.POST, queryset=product_medias)
        if product_new_data.is_valid() and product_medias_data.is_valid():
            product_instance = product_new_data.save()

            # Check if any  old file is deleted
            product_medias_data.save(commit=False)
            for deleted_object in product_medias_data.deleted_objects:
                deleted_object.delete()
            product_medias_data.save()

            # Adding new files
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "video/mp4"]
            max_size_mb = 2  # Max file size in MB
            max_size_bytes = max_size_mb * 1024 * 1024
            for file in request.FILES.getlist("files"):
                if file.size > max_size_bytes:
                    error_message = f"File size should not exceed {max_size_mb}MB."
                    messages.error(request, str(error_message))
                    product_form = ProductForm(instance=product_instance)
                elif file.content_type not in allowed_types:
                    error_message = (
                        "Invalid file type. Only JPEG, JPG, PNG, and MP4 are allowed."
                    )
                    messages.error(request, error_message)
                    product_form = ProductForm(instance=product_instance)
                else:
                    media_type = (
                        "image" if file.content_type.startswith("image") else "video"
                    )
                    Media.objects.create(
                        product=product_instance, file=file, media_type=media_type
                    ).save()
            logger.info(
                f"user {request.user.email} update product {product_instance.id}"
            )
            return redirect(
                "dashboard:product", product_id=product_id, product_slug=product_slug
            )
        else:
            messages.error(request, str(product_new_data.errors))
            messages.error(request, str(product_medias_data.errors))
            product_form = ProductForm(instance=product_instance)
    return render(
        request,
        "dashboard/product/edit_product.html",
        {
            "title": "Editing Product",
            "product_form": product_form,
            "product_medias": product_medias_forms,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def delete_product(request, product_slug):
    """Make the is_delete for the product to be true"""
    if request.method == "POST":
        product_id = request.POST.get("product")
        origin = request.POST.get("origin") or "dashboard:products"
        product = Product.objects.get(id=product_id)
        if product.is_deleted:
            return redirect("store:index")
        else:
            product.is_deleted = True
            product.save()
            return redirect(origin)
    else:
        return redirect("store:index")


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def erase_product(request, product_slug):
    """Erase Product form the System"""
    if request.method == "POST":
        product_id = request.POST.get("product")
        product = Product.objects.get(id=product_id)
        logger.info(f"user {request.user.email} erase product {product.id}")
        product.delete()
        return redirect("dashboard:products")
    else:
        return redirect("store:index")


# Department


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@is_auth
def get_departments(request):
    """Return Not deleted Departments"""

    departments = Department.objects.all()
    return render(
        request,
        "dashboard/departments.html",
        {
            "title": "Departments",
            "departments": departments,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def add_department(request):
    """Create New Department"""
    categories = Category.objects.filter(department=None)
    department_form = DepartmentForm()
    if request.method == "POST":
        department_image = request.FILES["image"]
        allowed_types = ["image/jpeg", "image/jpg", "image/png"]  # Allowed MIME types
        max_size_mb = 2  # Set max file size (in MB)
        max_size_bytes = max_size_mb * 1024 * 1024
        if department_image.size > max_size_bytes:
            error_message = f"Image size should not exceed {max_size_mb}MB."
            messages.error(request, error_message)
        elif department_image.content_type not in allowed_types:
            error_message = "Invalid file type. Only JPEG, JPG, and PNG are allowed."
            messages.error(request, error_message)
        else:
            department_data = DepartmentForm(request.POST, request.FILES)
            if department_data.is_valid():
                department_instance = department_data.save()
                for key, value in request.POST.items():
                    if "category" in key:
                        category = Category.objects.get(id=value)
                        if not category.department:
                            category.department = department_instance
                            category.save()
                department_instance.save()
                logger.info(
                    f"user {request.user.email} add department {department_instance.id}"
                )
                return redirect("dashboard:departments")
            else:
                messages.error(request, "Department Data is Not Valid")
                department_form = DepartmentForm(request.POST, request.FILES)

    return render(
        request,
        "dashboard/department/add_department.html",
        {
            "title": "Adding Department",
            "categories": categories,
            "department": department_form,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def edit_department(request, department_id, department_slug):
    """Edit A Department"""

    department = Department.objects.get(id=department_id)
    department_categories = department.category.all()
    department_less_categories = Category.objects.filter(department=None)
    categories = department_categories | department_less_categories

    department_form = DepartmentForm(instance=department)

    if request.method == "POST":
        department_image = request.FILES["image"]
        allowed_types = ["image/jpeg", "image/jpg", "image/png"]  # Allowed MIME types
        max_size_mb = 2  # Set max file size (in MB)
        max_size_bytes = max_size_mb * 1024 * 1024
        if department_image.size > max_size_bytes:
            error_message = f"Image size should not exceed {max_size_mb}MB."
            messages.error(request, error_message)
            department_form = DepartmentForm(instance=department)
        elif department_image.content_type not in allowed_types:
            error_message = "Invalid file type. Only JPEG, JPG, and PNG are allowed."
            messages.error(request, error_message)
            department_form = DepartmentForm(instance=department)
        else:
            new_data = DepartmentForm(request.POST, request.FILES, instance=department)
            if new_data.is_valid():
                updated_department = new_data.save(commit=False)
                new_cat = []
                for key, value in request.POST.items():
                    if "category" in key:
                        category = Category.objects.get(id=value)
                        new_cat.append(category)
                        if (
                            category not in department_categories
                            and category.department == None
                        ):
                            category.department = updated_department
                            category.save()

                for cat in department_categories:
                    if cat not in new_cat:
                        cat.department = None
                        cat.save()

                updated_department.save()
                logger.info(
                    f"user {request.user.email} edit department {department.id}"
                )
                return redirect("dashboard:departments")
            else:
                messages.error(request, "Department Data is Not Valid")
                department_form = DepartmentForm(
                    request.POST,
                    request.FILES,
                )

    return render(
        request,
        "dashboard/department/edit_department.html",
        {
            "title": f"Editing Department: {department.title}",
            "department": department,
            "categories": categories,
            "selected_categories": department_categories,
            "department_form": department_form,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def delete_department(request, department_slug):
    """Make the is_delete for the Department to be true"""

    if request.method == "POST":
        department_id = request.POST.get("department")
        department = Department.objects.get(id=department_id)
        if department.is_deleted:
            return redirect("store:index")
        else:
            department.is_deleted = True
            department.save()
            return redirect("dashboard:departments")
    else:
        return redirect("store:index")


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def erase_department(request, department_slug):
    """Erase Department form the System"""

    if request.method == "POST":
        department_id = request.POST.get("department")
        department = Department.objects.get(id=department_id)
        logger.info(f"user {request.user.email} erase department {department.id}")
        department.delete()
        return redirect("dashboard:departments")
    else:
        return redirect("store:index")


# Offer


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def add_offer(request, product_id, product_slug):
    """Add New new_offer"""
    product = Product.objects.get(id=product_id)
    if product.offer > 0:
        return redirect(
            "dashboard:product", product_id=product_id, product_slug=product_slug
        )
    if request.method == "POST":
        offer = request.POST.get("pof")
        if float(offer):
            product.offer = offer
            logger.info(f"user {request.user.email} add offer to product {product.id}")
            product.save()
            return redirect(
                "dashboard:product", product_id=product_id, product_slug=product_slug
            )
        else:
            messages.error(request, "حدث خطأ")
            return redirect(
                "dashboard:add-offer", product_id=product_id, product_slug=product_slug
            )
    return render(
        request,
        "dashboard/offer/offer.html",
        {
            "title": "Adding Offer",
            "product": product,
            # "breadcrumbs": breadcrumbs,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def edit_offer(request, product_id, product_slug):
    """ُEdit product offer"""

    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        offer = request.POST.get("pof")
        if float(offer) or int(offer) == 0:
            product.offer = offer
            product.save()
            logger.info(f"user {request.user.email} edit offer of product {product.id}")
            return redirect(
                "dashboard:product", product_id=product_id, product_slug=product_slug
            )
        else:
            messages.error(request, "حدث خطأ")
            return redirect(
                "dashboard:add-offer", product_id=product_id, product_slug=product_slug
            )

    return render(
        request,
        "dashboard/offer/offer.html",
        {
            "title": "Editing Offer",
            "product": product,
            # "breadcrumbs": breadcrumbs,
        },
    )


# Category


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def add_category(request):
    """Add New Category"""
    if request.method == "POST":
        new_category = CategoryForm(request.POST)
        if new_category.is_valid():
            category = new_category.save()
            logger.info(f"user {request.user.email} add category {category.id}")

            return redirect("dashboard:index")
        else:
            messages.error(request, str(new_category.errors))
            return redirect("dashboard:add-category")

    category_form = CategoryForm()
    return render(
        request,
        "dashboard/category/category.html",
        {
            "title": "Adding Category",
            "form": category_form,
            # "breadcrumbs": breadcrumbs,
        },
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def edit_category(request, category_id, category_slug):
    """Edit Category"""
    category = Category.objects.get(id=category_id)

    if request.method == "POST":
        new_category = CategoryForm(request.POST, instance=category)
        if new_category.is_valid():
            category = new_category.save()
            category.department.save()
            logger.info(f"user {request.user.email} edit category {category.id}")
            return redirect("dashboard:index")
        else:
            messages.error(request, str(new_category.errors))
            return redirect("dashboard:edit-category", category_id, category_slug)

    category_form = CategoryForm(instance=category)
    return render(
        request,
        "dashboard/category/category.html",
        {"title": "Editing Category", "form": category_form},
    )


@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@is_auth
def erase_category(request, category_slug):
    """Erase Category form the System"""

    if request.method == "POST":
        category_id = request.POST.get("category")
        origin = request.POST.get("origin")
        category = Category.objects.get(id=category_id)
        department = category.department
        logger.info(f"user {request.user.email} delete category {category.id}")
        category.delete()
        department.save()
        return redirect(origin)
    else:
        return redirect("store:index")


# @ratelimit(key="ip", rate="10/m", method="GET", block=True)
# @is_auth
# @is_admin
# def visitors_analytics(request):
#     activate("ar")
#     ordering_kw = request.GET.get("vord") or "lv"
#     if str(request.GET.get("vpp")).isdigit() and int(request.GET.get("vpp")) >= 1:
#         visitors_per_page = request.GET.get("vpp")
#     else:
#         visitors_per_page = 50

#     visitors = Visitor.objects.all()

#     if ordering_kw == "lv":
#         visitors = visitors.order_by("-visit_time")
#     elif ordering_kw == "ov":
#         visitors = visitors.order_by("visit_time")
#     elif ordering_kw == "ip":
#         visitors = visitors.order_by("ip")
#     elif ordering_kw == "cntry":
#         visitors = visitors.order_by("country")
#     elif ordering_kw == "cty":
#         visitors = visitors.order_by("city")

#     return render(
#         request,
#         "dashboard/reports/visitors_analytics.html",
#         {
#             "title": "الزوار",
#             "visitors": visitors[: int(visitors_per_page)],
#         },
#     )
