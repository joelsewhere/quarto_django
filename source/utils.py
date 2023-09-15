from pathlib import Path
from jinja2 import Template

root = Path(__file__).resolve().parents[1]
projects = root / 'projects'

def get_index_paths(filetype):
    return list(projects.rglob(f'*/*/*index.{filetype}'))

def render_template(template, params={}):

    template_path = root / 'templates' / template

    with template_path.open('r') as file:
        template = file.read()

    return Template(template)

def get_project_subpath(file):
    """
    Isolates the section of a filepath
    that comes after the "parent" directory.
    """
    for idx, parent in enumerate(file.parents):
        if parent.name == 'projects':
            break
    subpath = '/'.join(file.parts[-(idx + 1):])
    return subpath