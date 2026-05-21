from django.core.exceptions import PermissionDenied
from functools import wraps

def moderator_required(view_func):
    """Chỉ Moderator hoặc Admin mới được vào"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('accounts:login')
        if not request.user.is_mod_or_admin():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper