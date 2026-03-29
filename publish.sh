#!/bin/bash
# this_file: publish.sh
set -eu

echo "Cleaning previous builds..."
rm -rf dist/ build/

echo "Building wheels..."
uvx hatch build

echo "Publishing to PyPI..."
uv publish dist/*

echo "✓ Publish complete"
