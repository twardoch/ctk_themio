#!/usr/bin/env bash
# install.sh — Install ctk_themio locally
# ctk_themio is a visual WYSIWYG theme editor for CustomTkinter applications
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing ctk_themio..."
uv pip install -e . 2>/dev/null || pip install -e . 2>/dev/null || echo "Install failed"
echo "Done."
