from django.utils.timezone import now
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from dashboard.filters import ProductFilter
from .models import User


def order_products(ordering_kw, products):
    """
    la: last add products
    of: oldest first products
    dp: discount
    dpr: discount reverse
    hp: highest price
    lp: lowest price
    """

    if ordering_kw == "la":
        ordered_products = products.order_by("created_at").reverse()
    elif ordering_kw == "of":
        ordered_products = products.order_by("created_at")
    elif ordering_kw == "dp":
        ordered_products = products.order_by("offer")
    elif ordering_kw == "dpr":
        ordered_products = products.order_by("offer").reverse()
    elif ordering_kw == "hp":
        ordered_products = products.order_by("price").reverse()
    elif ordering_kw == "lp":
        ordered_products = products.order_by("price")
    else:
        return products
    return ordered_products


def filtering(request, products):
    """"""

    filter_form = ProductFilter(request.GET, queryset=products)
    return filter_form


def paging(request, products, list_len=None):
    """"""
    ordering_kw = request.GET.get("pord") or "la"

    if str(request.GET.get("ppp")).isdigit() and int(request.GET.get("ppp")) >= 1:
        list_length = request.GET.get("ppp")
    elif list_len:
        list_length = list_len
    else:
        list_length = 24

    if str(request.GET.get("page")).isdigit() and int(request.GET.get("page")) >= 1:
        page_number = request.GET.get("page")
    else:
        page_number = 1

    ordered_products = order_products(ordering_kw, products)
    filter_form = filtering(request, ordered_products)

    if filter_form.data:
        ordered_products = filter_form.qs

    paginator = Paginator(ordered_products, list_length)
    page_obj = paginator.get_page(page_number)

    return page_obj


def get_logged_in_users():
    active_sessions = Session.objects.filter(expire_date__gte=now())
    logged_users_ids = [
        session.get_decoded().get("_auth_user_id") for session in active_sessions
    ]
    return User.objects.filter(id__in=logged_users_ids)


def is_logged_in(user):
    active_sessions = Session.objects.filter(expire_date__gte=now())
    for session in active_sessions:
        data = session.get_decoded()
        if str(user.id) == str(data.get("_auth_user_id")):
            return (True, session)
    else:
        return (False, 0)


def user_logout(user):
    if is_logged_in(user)[0]:
        is_logged_in(user)[1].delete()
