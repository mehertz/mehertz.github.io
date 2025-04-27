# Static Site Generator

A simple, lightweight static site generator built with Python.

## Features

- Markdown to HTML conversion
- YAML front matter for metadata
- Jinja2 templating
- Static file handling
- Simple command-line interface
- Reproducible builds with uv

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd website
```

### Quick Setup (recommended)

```bash
# Run the setup script (installs uv, dependencies & package)
./scripts/setup_env.sh

# Activate the virtual environment
source .venv/bin/activate
```

### Traditional installation

If you prefer pip:

```bash
python -m pip install -e .
```

## Usage

### Directory Structure

```
website/
├── content/          # Markdown content files
├── ssg/
│   ├── templates/    # Jinja2 HTML templates
│   └── static/       # Static files (CSS, JavaScript, images)
├── html/             # Generated site (created on build)
├── pyproject.toml    # Modern Python packaging
├── requirements.txt  # Pinned dependencies for reproducibility
└── .uv/              # uv configuration for reproducible builds
```

### Creating Content

Create Markdown files in the `content` directory with YAML front matter:

```markdown
---
title: My Page Title
template: page.html
date: 2023-09-13
---

# My Page Content

This is a paragraph.
```

### Building the Site

From the project directory, run:

```bash
ssg
```

Or with custom paths:

```bash
ssg --content content/ --templates ssg/templates/ --static ssg/static/ --output html/
```

### Serving the Site

You can use Python's built-in HTTP server to preview the site:

```bash
cd html
python -m http.server
```

Then open your browser to http://localhost:8000

## Templates

The default template is `page.html`. You can create additional templates in the `ssg/templates` directory.

Available variables in templates:

- `content`: The HTML content converted from Markdown
- All front matter variables (e.g., `title`, `date`)

## Reproducibility

This project uses uv's lockfile feature to ensure reproducible builds. To update dependencies while maintaining reproducibility:

```bash
# Update dependencies and regenerate lockfile
uv pip install -r requirements.txt --upgrade
```

## License

MIT 