import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring_systems.settings')
django.setup()

from authentication.models import User
from monitoring.models import Machine

def create_initial_data():
    # Создаём пользователя
    if not User.objects.filter(username="admin").exists():
        user = User(username="admin")
        user.set_password("password123")
        user.save()
        print("✅ Created admin user")

    # Создаём 30 тестовых машин
    for i in range(1, 31):
        name = f"server-{i}"
        if not Machine.objects.filter(name=name).exists():
            Machine.objects.create(
                name=name,
                ip_address=f"192.168.1.{i}",
                endpoint_url="http://mock_server:8001"
            )
            print(f"✅ Created machine: {name}")

if __name__ == "__main__":
    create_initial_data()