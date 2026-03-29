# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CTk Theme Builder (`ctk_themio`) is a GUI application for creating, designing, and managing custom themes for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). It provides WYSIWYG visual editing with a live preview panel showing theme effects across all 18+ supported CTk widgets.

Published to PyPI as `ctk_themio`. Target: Python >= 3.13.

## Build & Run

```bash
# Install in development mode
uv pip install -e .

# Run the app (three ways)
ctk-themio                           # console entry point
python -m ctk_themio                 # module execution
ctk-themio -a Dark -t theme.json     # preview-only mode

# Run the demo
ctk-themio-demo

# Build wheel
uvx hatch build

# Publish to PyPI
./publish.sh
```

## Package Structure

Standard `src/` layout with `hatch` build system and `hatch-vcs` for git-tag semver.

```
src/ctk_themio/
  __init__.py          # package root, version via importlib.metadata
  __main__.py          # python -m ctk_themio entry point
  paths.py             # centralized path definitions (platformdirs)
  controller/          # CLI arg parsing, app launch
  model/               # business logic, preferences DB
  view/                # all GUI: control panel, preview, dialogs
  utils/               # color utilities, logging, constants
  assets/              # bundled JSON configs, themes, images (read-only)
  user_themes/         # bundled sample themes (copied to user data on first run)
  demo/                # widget showcase app (app.py + data/)
```

## Path Management

All paths are centralized in `ctk_themio/paths.py`. User-writable data uses OS-appropriate directories via `platformdirs`:

- **Read-only** (in package): `ASSETS_DIR`, `CONFIG_DIR`, `ETC_DIR`, `VIEWS_DIR`, `APP_THEMES_DIR`, `APP_IMAGES`
- **User-writable** (via platformdirs): `DB_FILE_PATH`, `LOG_DIR`, `TEMP_DIR`, `PALETTES_DIR`, `USER_DATA_DIR`

The database auto-initializes on first run via `init_db()` in `preferences.py`.

## Architecture (MVC)

- **`controller/ctk_theme_builder.py`** - Entry point with `main()`. Parses CLI args (`-a` appearance, `-t` theme file). Launches `ControlPanel` (editor) or `PreviewPanel` (preview-only).
- **`model/ctk_theme_builder.py`** (~1200 lines) - Core logic: theme loading/saving, `CommandStack` undo/redo, `@log_call` decorator.
- **`model/preferences.py`** - SQLite CRUD for user preferences. Tables: `preferences`, `application_control`, `colour_palette_entries`, `colour_cascade_properties`.
- **`view/control_panel.py`** (~2575 lines) - Main window. Imports all dialogs and the preview panel.
- **`view/ctk_theme_preview.py`** (~1300 lines) - Live preview of all CTk widgets.
- **`view/`** - Dialogs: `harmonics_dialog.py`, `geometry_dialog.py`, `preferences.py`, `export_import.py`, `theme_merger.py`, `provenance_dialog.py`, `about.py`.
- **`utils/cbtk_kit.py`** (~817 lines) - Color utilities: hex/rgb conversion, shading, contrast.
- **`utils/loggerutl.py`** - `LogGen` wrapping loguru. Logs to platformdirs user log directory.
- **`demo/app.py`** (~2000 lines) - 13-tab widget showcase with graceful optional dependency handling.

## Import Convention

All internal imports use absolute package paths:
```python
from ctk_themio.model.ctk_theme_builder import log_call
from ctk_themio.view.control_panel import ControlPanel
from ctk_themio.utils.cbtk_kit import shade_hex_colour
```

## Theme Data Format

Themes are JSON files mirroring CustomTkinter widget properties:
- Color values: `[light_mode, dark_mode]` pairs or single values
- Properties: **color** (fg_color, bg_color, hover_color...) and **geometry** (border_width, corner_radius...)
- View schemas (`assets/views/Basic.json`, `Categorised.json`) define widget-to-property mappings
- Built-in themes in `assets/themes/`, user themes in `user_themes/`

## Key Assets

| Path (relative to `src/ctk_themio/`) | Purpose |
|---------------------------------------|---------|
| `assets/themes/` | 14 built-in theme JSON files |
| `assets/etc/theme_skeleton.json` | Template for new themes |
| `assets/etc/geometry_parameters.json` | Default geometry values |
| `assets/views/Basic.json` | Widget-to-property mapping schema |
| `assets/config/repo_updates.json` | Database migration definitions |
| `assets/images/` | App icons and UI graphics |
| `demo/data/` | Demo images and video |

## Known CTk Workarounds

- `FORCE_GEOM_REFRESH_PROPERTIES` - Properties requiring full preview refresh due to CTk rendering issues
- `FORCE_COLOR_REFRESH_PROPERTIES` - Color properties that don't update without manual refresh

## Key Dependencies

`customtkinter>=5.2.2` (core), `colorharmonies` (color schemes), `loguru` (logging), `matplotlib` (color utilities), `pillow` (images), `pyperclip` (clipboard), `CTkMessagebox`/`CTkToolTip` (UI widgets), `pathvalidate`, `darkdetect`, `fonttools`. Full list in `pyproject.toml`.
