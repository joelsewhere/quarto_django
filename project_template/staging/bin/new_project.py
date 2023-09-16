from pathlib import Path

template = """---
title: "{title}"
listing:
  contents: .
  sort: "date desc"
  type: default
  categories: true
  sort-ui: true
  filter-ui: true
page-layout: full
title-block-banner: true
---
"""

root = Path(__file__).parents[1]
projects = root / 'projects'

project_name = input("\n\n\x1B[34mProject title:\x1B[0m\n")
dir_name = project_name.replace(' ', '_').strip().lower()

project_dir = projects / dir_name
project_dir.mkdir(parents=True, exist_ok=True)

index_file = project_dir / 'index.qmd'

index_file.write_text(template.format(title=project_name))
print(f"\n\n\x1B[34mNew project created at {project_dir.as_posix()}\x1B[0m\n")
