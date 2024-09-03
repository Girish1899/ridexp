from django.shortcuts import redirect
from django.urls import reverse

class SuperAdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/quality/') and request.session.get('user_type')!="quality":
            return redirect(reverse('login'))  # Redirect to the home page or any other page
        response = self.get_response(request)
        return response