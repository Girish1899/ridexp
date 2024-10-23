from django.shortcuts import redirect
from django.urls import reverse

class SuperAdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/superadmin/') and not request.user.is_superuser and request.session.get('user_type')!="Superadmin":
            return redirect(reverse('login'))  
        response = self.get_response(request)
        return response