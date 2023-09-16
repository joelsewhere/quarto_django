from pathlib import Path 
import shutil
import sys

# Root project path
root = Path(__file__).resolve().parents[2]
# Add to import path
sys.path.append(root.as_posix())

# Import utils
from source import utils

# site_ paths
site = root / '_site'
projects = site / 'projects'
site_libs = site / 'site_libs'
about = site / 'about.html'
index = site / 'index.html'
profile = site / 'profile.jpg'
styles = site / 'styles.css'

# django paths
django = root / 'django_site' / 'quarto'
django_static = django / 'static'
django_templates = django / 'templates'

# recursive search for index_files
index_files = []
for path in projects.rglob('*'):
    if path.is_dir() and path.name == 'index_files':
        index_files += [x for x in path.rglob('*') if not x.is_dir()]

# copy index files to django_static
for file in index_files:
    subpath = utils.get_project_subpath(file)
    file_path = django_static / 'projects' / Path(subpath)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(file.as_posix(), file_path.as_posix())

# copy files
(django_templates / 'projects').mkdir(parents=True, exist_ok=True)
(django_static / 'projects').mkdir(parents=True, exist_ok=True)
shutil.copytree(site_libs.as_posix(), (django_static/'site_libs').as_posix(), dirs_exist_ok=True)
shutil.copy(about.as_posix(), (django_templates/ 'about.html').as_posix())
shutil.copy(index.as_posix(), (django_templates/ 'projects'/ 'index.html').as_posix())
shutil.copy(profile.as_posix(), (django_static/'site_libs/profile.jpg').as_posix())
shutil.copy(styles.as_posix(), (django_static/'styles.css').as_posix())
shutil.copytree(projects.as_posix(), (django_templates/'projects').as_posix(), dirs_exist_ok=True)
