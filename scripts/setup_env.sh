#!/bin/bash
# This script sets up a reproducible development environment using uv

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Source the shell to make uv available
    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    elif [ -f ~/.zshrc ]; then
        source ~/.zshrc
    else
        echo "Please restart your shell to use uv"
        exit 1
    fi
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv

# Install dependencies
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Install the package in development mode
echo "Installing the package..."
uv pip install -e .

echo "✅ Environment setup complete!"
echo "→ Activate with: source .venv/bin/activate" 