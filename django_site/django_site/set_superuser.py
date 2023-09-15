import sys
import os
import django
from pathlib import Path 


cwd = Path(__file__).resolve().parent
sys.path.append(cwd.parent.as_posix())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_site.settings')

django.setup()

from quarto.models import AppUser

args = sys.argv

email = args[1]
user, created = AppUser.objects.get_or_create(email=email)
user.is_staff = True
user.is_admin = True
user.is_superuser = True
user.save()