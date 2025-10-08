from django.shortcuts import render, redirect
from django.utils import timezone
from authentication.models import User, UserSession
import secrets

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    token = secrets.token_urlsafe(32)
                    
                    expires_at = timezone.now() + timezone.timedelta(hours=1)

                    UserSession.objects.create(
                        user=user,
                        session_token=token,
                        expires_at=expires_at  # ← теперь это datetime
                    )
                    response = redirect('dashboard')
                    response.set_cookie('session_token', token, httponly=True, max_age=3600)
                    return response
            except User.DoesNotExist:
                pass

        return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

def dashboard_view(request):
    if not hasattr(request, 'user') or not request.user:
        return redirect('login')
    return render(request, 'dashboard.html')