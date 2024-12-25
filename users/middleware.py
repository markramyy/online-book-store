from django.http import HttpResponseForbidden


def customer_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_customer:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return func(request, *args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return func(request, *args, **kwargs)
    return wrapper
