from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    LOGIN_EXEMPT_URLS = [
        reverse('purchase_app:auth_login'),
        reverse('purchase_app:sign_up'),
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in self.LOGIN_EXEMPT_URLS):
            return redirect(reverse('purchase_app:auth_login'))

        response = self.get_response(request)
        return response
