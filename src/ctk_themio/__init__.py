# this_file: src/ctk_themio/__init__.py
"""
CTk Theme Builder: A visual theme editor for CustomTkinter applications.

This package provides a WYSIWYG editor to create, modify, and preview themes 
for the CustomTkinter UI framework. It supports live preview across all 18+ 
built-in widgets, color harmonic generation, and theme merging.

Entry points:
    ctk-themio: Run the main theme editor application.
    ctk-themio-demo: Run a comprehensive widget showcase application.
"""

try:
    from importlib.metadata import version
    __version__ = version("ctk_themio")
except Exception:
    __version__ = "0.0.0"

# Initialize paths and create runtime directories.
# We do this at the package level to ensure user data directories
# exist before any submodules try to write to them.
import ctk_themio.paths  # noqa: F401, E402
