from django.contrib.auth import login
from django.contrib.auth.models import User

from .remember import COOKIE_NAME, parse_token


class RememberMeMiddleware:
    """Auto-login from the remember_token cookie, if present and valid."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            token = request.COOKIES.get(COOKIE_NAME)
            if token:
                username = parse_token(token)
                if username:
                    try:
                        user = User.objects.get(username=username)
                        login(request, user)
                    except User.DoesNotExist:
                        pass
        return self.get_response(request)
