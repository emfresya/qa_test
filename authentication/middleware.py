from django.utils import timezone
from .models import UserSession

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('session_token')
        if token:
            try:
                session = UserSession.objects.get(
                    session_token=token,
                    expires_at__gt=timezone.now()
                )
                request.user = session.user
            except UserSession.DoesNotExist:
                request.user = None
        else:
            request.user = None

        response = self.get_response(request)
        return response