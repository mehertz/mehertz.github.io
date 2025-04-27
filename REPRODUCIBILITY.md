# Ensuring Reproducibility with uv

This project uses [uv](https://github.com/astral-sh/uv) to ensure reproducible builds. uv is a fast Python package installer and resolver that supports lockfiles for reproducibility.

## Quick Setup

The simplest way to set up your environment is to use our setup script, which handles everything for you:

```bash
./scripts/setup_env.sh
```

This will:
1. Install uv if not already installed
2. Create a virtual environment in `.venv`
3. Install dependencies from `requirements.txt`
4. Install the package in development mode

After running the script, activate the environment:

```bash
source .venv/bin/activate
```

## Manual Setup

If you prefer to set up the environment manually:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Install the package in development mode
uv pip install -e .
```

## Reproducibility features

This project uses the following uv features to ensure reproducibility:

1. **Pinned dependencies**: All dependencies in `requirements.txt` have exact versions.

2. **Lockfiles**: The project uses uv's lockfile feature (stored in `.uv/lockfile.txt`) to pin all dependencies, including transitive ones, ensuring consistent builds across environments.

3. **Hash-based dependencies**: The `.uv/settings.toml` configuration enables hash-based dependencies, providing additional verification of package contents.

## Updating dependencies

To update dependencies while maintaining reproducibility:

```bash
# Update dependencies and regenerate lockfile
uv pip install -r requirements.txt --upgrade

# If you want to update a specific package
uv pip install package_name==new_version
uv pip freeze > requirements.txt
```

## How it works with modern Python packaging

The project uses both `pyproject.toml` (for modern Python packaging) and `setup.py` (for backward compatibility). When installing with uv, the modern packaging approach is used. 