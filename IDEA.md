# Future Ideas

## Completed (v4.0.0)

- [x] Reorganize repo into standard Python package inside `src/ctk_themio/`
- [x] Remove obsolete build scaffolding
- [x] Make launch entry point in `src/ctk_themio/__main__.py` and `ctk_themio` script
- [x] Create standard `pyproject.toml`
- [x] Configure build system around `hatch`
- [x] Add hatch-vcs for git-tag-based semver
- [x] Write `publish.sh` using `uvx hatch` to build and `uv publish` to publish
- [x] Configure for Python >= 3.13
- [x] Port `_private/ctkdemo.py` and `_private/ctkdemo_data` into the package
- [x] Use platformdirs for OS-appropriate user data locations

## Completed (v2.0.5)

- [x] Write functional tests (headless suite for colour maths, preferences, paths, migration)
- [x] Set up CI/CD (GitHub Actions: lint, type-check, test on Linux + macOS; tag-triggered PyPI release)
- [x] Fix the v4→v5 theme migrator (widget-key casing crash; import-time argv parsing)

## Remaining

- [ ] Add comprehensive type hints and docstrings across the codebase (headless modules done; `view/` still untyped)
- [ ] Investigate CustomTkinter 5.2.2 compatibility issues with Python 3.13 (TclError in widget _draw callbacks)
- [ ] Refactor large modules (control_panel.py ~2575 lines, ctk_theme_preview.py ~1300 lines)
- [ ] Consider splitting the demo app.py (2000+ lines) into tab modules
