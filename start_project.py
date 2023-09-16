from pathlib import Path
from jinja2 import Template
import shutil

auth_key = ''
auth_secret = ''
title = input("\n\n\x1B[34mPlease enter a project title:\x1B[0m\n")
group_permissions = input('\x1B[34mDo you want to use group permissioning? [y/N]\x1B[0m\n').strip().lower() == 'y'
social_auth = input("\x1B[34mDo you want to use google auth for user authentication? [y/N]\x1B[0m\n").strip().lower() == 'y'
if social_auth:
    print('''\n\x1B[1;41m
          You will now be prompted to enter your google auth keys. 
          (See https://developers.google.com/identity/protocols/oauth2 for instructions)

          If you do not have google auth keys, you can set this up later.
          To set this up later, hit enter for each prompt. 
          If setting up later, you will need to manually edit
          the following variables in django_site/django_site/settings.py
            - SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
            - SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET\x1B[0m\n\n''')
    auth_secret = input('\x1B[34mPlease provide your GOOGLE_OAUTH2_SECRET:\x1B[0m\n')
    auth_key = input('\x1B[34mPlease provide your GOOGLE_OAUTH2_KEY:\x1B[0m\n')
share_links = input("\x1B[34mDo you want to add a share link at the top of each report? [y/N]\x1B[0m\n").strip().lower() == 'y'
if share_links and not social_auth:
    print("\x1B[31mShare links are only available for logged in users, and will not appear in your project until user authentication is implemented\x1B[0m")

root = Path(__file__).resolve().parent
template_root = root / 'project_template'
staging = root / title.lower().strip().replace(' ', '_')
staging.mkdir(exist_ok=True)
django = template_root / 'django_site'

alternates = [
    'set_django_html.py',
    'update_department_model.py',
    'index_template.html'
    ]

templates = [
    template_root / '_quarto.yml',
    django / 'django_site' /  '.env',
    django / 'django_site' / 'settings.py',
    django / 'django_site' / 'urls.py',
    django / 'quarto' / 'admin.py',
    django / 'quarto' / 'forms.py',
    django / 'quarto' / 'models.py',
    django / 'quarto' / 'urls.py',
    django / 'quarto' / 'views.py'
    ]

def get_subpath(file, root):

    if file.parent == root:
        return file.name
    for idx, parent in enumerate(file.parents):
        if parent == root:
            break
    subpath = '/'.join(file.parts[-(idx + 1):])
    return subpath


for template in templates:

    text = template.read_text()
    try:
        jinja = Template(text)
    except:
        raise ValueError(f'{template.as_posix()}')
    
    updated_text = jinja.render(
        project_title=title,
        use_group_permissions=group_permissions,
        use_share_links=share_links,
        use_social_auth=social_auth,
        auth_key=auth_key,
        auth_secret=auth_secret
        )
    new_path = staging / get_subpath(template, template_root)
    new_path.parent.mkdir(parents=True, exist_ok=True)
    new_path.write_text(updated_text)

scripts = template_root / 'scripts'

if share_links:
    set_django_html = scripts / 'post_render' / 'set_django_html.py'
else:
    set_django_html = scripts / 'post_render' / 'set_django_html_alternative.py'
new_path = staging / get_subpath(set_django_html, template_root)
new_path.parent.mkdir(parents=True, exist_ok=True)
shutil.copy(set_django_html.as_posix(), new_path.as_posix())
new_path.rename(new_path.parent / 'set_django_html.py')

if group_permissions:
    old_path = scripts/ 'post_render' / 'update_department_model.py'
    new_path = staging / get_subpath(old_path, template_root)
    new_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(old_path.as_posix(), new_path.as_posix())

index_template = template_root / 'templates' / 'index_template.html'
text = index_template.read_text()
addon = f"""---
title: { title }\n"""
text = addon + text
new_path = (staging / get_subpath(index_template, template_root))
new_path.parent.mkdir(parents=True, exist_ok=True)
new_path.write_text(text)

all_paths = template_root.rglob('*')
staging_paths = [get_subpath(x, staging) for x in staging.rglob('*')]

for path in all_paths:
    if 'staging' in path.as_posix():
        continue
    if 'project_template' not in path.as_posix():
        continue
    no_template_root = get_subpath(path, template_root)
    new_path = (staging / no_template_root)
    if new_path.exists():
        continue
    if no_template_root in staging_paths:
        continue
    elif path.is_dir():
        new_path.mkdir(parents=True, exist_ok=True)
    else:
        new_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(path.as_posix(), new_path.as_posix())
print('\x1B[34mProject created!\x1B[0m')

