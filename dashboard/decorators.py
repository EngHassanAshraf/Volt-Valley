from django.shortcuts import redirect


def is_not_auth(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:index")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def is_auth(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("mainpages:index")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def is_admin(view_func):
    def wrapper(request, *args, **kwargs):
        for group in request.user.groups.all():
            if group.name == "admin":
                return view_func(request, *args, **kwargs)
        else:
            return redirect("dashboard:index")

    return wrapper


# def user_permissions(allowed=[]):
#     def decorator(view_func):
#         def wrapper(request, *args, **kwargs):
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name
#                 if group in allowed:
#                     return view_func(request, *args, **kwargs)
#             return redirect("mainpages:index")
#         return wrapper
#     return decorator
