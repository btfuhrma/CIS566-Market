from django.apps import AppConfig
from django.contrib.auth import get_user_model

class AppUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_user'

    def ready(self):
        User = get_user_model()
        email = 'admin'  # Specify your admin email
        password = 'password'    # Specify your admin password

        # Check if the admin user exists
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
