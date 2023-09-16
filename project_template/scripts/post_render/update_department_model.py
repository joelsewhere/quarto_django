"""
This script is only needed for the default group permissioning
provided with this project. If group permissions for particular projects
is not needed, this file can be deleted. If this file is deleted, be sure to
remove the line linking to this filename (update_department_model.py) in 
the root/_quarto.yml file. 
"""

import os
import django
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
django_path = root / 'django_site'
site = root / '_site'
projects = site / 'projects'

sys.path.append(django_path.as_posix())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_site.settings')
django.setup()

from quarto.models import Project

departments = [x.name for x in projects.iterdir() if x.is_dir()]
for department_ in departments:

    department, created = Project.objects.get_or_create(name=department_)
    department.save()
