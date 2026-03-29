# this_file: src/ctk_themio/__init__.py
"""CTk Theme Builder - Visual theme editor for CustomTkinter applications."""

try:
    from importlib.metadata import version
    __version__ = version("ctk_themio")
except Exception:
    __version__ = "0.0.0"

# Initialize paths and create runtime directories
import ctk_themio.paths  # noqa: F401, E402
