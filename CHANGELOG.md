# Changelog

## v2.0.5 (2026-07-05) - Tooling, tests, CI, and a migrator fix

First pass of the portfolio modernisation. No behaviour change for the GUI; the
headless logic is now tested and the project has continuous integration.

### Fixed

- **Theme migrator crash.** `utils/ctk_theme_migrate.py` wrote to `CTkCheckbox`
  and `CTkRadiobutton`, but CustomTkinter v5 (and the bundled skeleton) use
  `CTkCheckBox` and `CTkRadioButton`. Every conversion raised `KeyError`. Fixed
  the casing so v4→v5 migration completes.
- **Import-time crash in the migrator.** The module parsed `argv` and validated
  files at import, so `import ctk_themio.utils.ctk_theme_migrate` failed. Moved
  the CLI into a guarded `main()`; `ThemeConverter` is now importable and tested.
- Repaired a mangled module docstring in `model/preferences.py` (literal `n`
  characters where line breaks belonged).

### Added

- **Test suite** (`tests/`, 29 tests, headless): colour maths and geometry
  helpers in `cbtk_kit`, the SQLite preference store round-trip, the path map,
  and a functional v4→v5 migration.
- **CI** (`.github/workflows/ci.yml`): ruff lint + format check, mypy on the
  headless modules, and pytest on Linux (under `xvfb`) and macOS.
- **Release workflow** (`.github/workflows/release.yml`): tag-triggered build
  and PyPI publish via trusted publishing.
- Project icon at `docs/assets/icon.png`.
- Jekyll + Just the Docs documentation site under `docs/` with a Theme schema
  reference.

### Changed

- Added `ruff`, `mypy`, and `pytest` configuration to `pyproject.toml`, plus a
  `dev` dependency group. Ruff and mypy pass clean.
- Added type hints and light annotations to the headless modules; replaced the
  six `from CTkToolTip import *` star imports with explicit imports.

## v4.0.0 (2026-03-29) - Modern Python Package Refactoring

Complete restructuring from a script-based project into a standard, installable Python package.

### Package Structure

- Reorganized entire codebase into `src/ctk_themio/` standard layout
- Created `pyproject.toml` with `hatchling` build system and `hatch-vcs` for git-tag-based semantic versioning
- Added `__init__.py` (package root with version via `importlib.metadata`) and `__main__.py` (enables `python -m ctk_themio`)
- Configured console entry points: `ctk-themio` (main app) and `ctk-themio-demo` (widget showcase)
- Target: Python >= 3.13, publishable to PyPI as `ctk_themio`

### Import System

- Converted all 59 internal imports across 15 source files from bare subpackage style (`from model.X import Y`) to absolute package imports (`from ctk_themio.model.X import Y`)
- Removed `sys.path` manipulation hacks from all four subpackage `__init__.py` files
- Created centralized `ctk_themio.paths` module for all path definitions

### User Data (platformdirs)

- Migrated all user-writable directories to OS-appropriate locations via `platformdirs`:
  - Database: `~/Library/Application Support/ctk_themio/` (macOS)
  - Logs: `~/Library/Logs/ctk_themio/`
  - Cache/temp: `~/Library/Caches/ctk_themio/tmp/`
  - Palettes: `~/Library/Application Support/ctk_themio/palettes/`
  - User themes: `~/Library/Application Support/ctk_themio/user_themes/`
- Bundled read-only assets (themes, images, configs, views) remain inside the package
- First-run auto-copies bundled user themes to user data directory

### Database Initialization

- Added automatic SQLite database creation on first run (`init_db` in `preferences.py`)
- Creates all required tables: `preferences`, `application_control`, `colour_palette_entries`, `colour_cascade_properties`
- Auto-applies seed data from `repo_updates.json` migrations
- `preference_setting()` now returns default values gracefully when DB is missing (instead of raising `FileNotFoundError`)

### Application Launch

- Extracted `main()` function in controller for use as console entry point
- Preview panel now launches via `python -m ctk_themio` subprocess (replaces old shell/batch scripts)
- App window brought to foreground on launch (lift + topmost + focus_force)

### Demo Application

- Ported `_private/ctkdemo.py` (2000+ line widget showcase) into `src/ctk_themio/demo/`
- Included demo data files (images, video) in `demo/data/`
- Accessible via `ctk-themio-demo` console entry point

### Removed

- `build_app.sh` / `build_app.bat` (replaced by `hatch build`)
- `ctk_theme_builder.sh` / `ctk_theme_builder.bat` (replaced by `ctk-themio` entry point)
- `requirements.txt` (replaced by `pyproject.toml` dependencies)
- `theme_builder_setup.py` (replaced by auto-initialization)
- `get-pip.py` (obsolete)
- Shell/batch launcher scripts in `utils/`

### Added

- `pyproject.toml` - modern build configuration
- `publish.sh` - build and publish to PyPI
- `CLAUDE.md` - AI coding assistant guidance
- `CHANGELOG.md` - this file
- `platformdirs` dependency for OS-appropriate data directories
