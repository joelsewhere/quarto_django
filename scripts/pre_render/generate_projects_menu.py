from pathlib import Path
from jinja2 import Template
import matplotlib.pyplot as plt

# root project path
root = Path(__file__).resolve().parents[2]

# template file that generates the root/index.qdm file
template = root / 'templates' / 'index_template.html'

# all top-level directories within root/projects will be listed
projects = root / 'projects'
project_paths = []
for project in projects.iterdir():
    if project.is_dir():
        path = Path(*project.parts[-2:])
        project_paths.append(path)

# Using matplotlib's default color theme to color each project directory
colors = list(plt.rcParams['axes.prop_cycle'].by_key()['color'])

# list of dictionaires used by the index_template
# to generate the projects menu
template_fields = []
for path, color in zip(project_paths, colors):
    template_field = {
        "href": path.as_posix(),
        "name": path.name.replace('_', ' ').title(),
        "color": color
        }
    template_fields.append(template_field)

# template file
with template.open('r') as file:
    template = file.read() 

# final root/index.qdm file
index = Template(template).render(projects=template_fields)

with (root/'index.qmd').open('w') as file:
    file.write(index)
