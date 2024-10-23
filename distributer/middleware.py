from django.shortcuts import redirect
from django.urls import reverse

class distributerCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/distributer/') and request.session.get('user_type')!="distributer":
            return redirect(reverse('login'))  
        response = self.get_response(request)
        return response