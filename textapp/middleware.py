# your_app/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # These are exact public paths (reverse resolves to full URL path)
        self.public_paths = [
            reverse('login'),
            reverse('register'), # Add more like reverse('password_reset') if needed
        ]

        # These are path prefixes that should always be accessible
        self.exempt_startswith = [
            '/static/', 
            '/media/', 
            '/admin/', 
            '/favicon.ico', 
        ]

    def __call__(self, request):
        path = request.path

        # Allow exempt prefixes
        if any(path.startswith(prefix) for prefix in self.exempt_startswith):
            return self.get_response(request)

        # Block access to login/register if already logged in
        if request.user.is_authenticated and path in self.public_paths:
            return redirect('home')

        # Block unauthenticated users from accessing anything else
        if not request.user.is_authenticated and path not in self.public_paths:
            return redirect('login')

        return self.get_response(request)
