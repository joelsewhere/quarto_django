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

if len(args) > 1:
    email = args[1]
    if len(args) > 2:
        password = args[2]
    else:
        password = 'password'
    user, created = AppUser.objects.get_or_create(email=email, password=password) 
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save()