# TODO

Flat task list. Bigger ideas live in `IDEA.md`; shipped work moves to `CHANGELOG.md`.

## Tests & correctness

- [ ] Widen headless coverage of `model/ctk_theme_builder.py` — the `CommandStack` undo/redo logic is pure and untested.
- [ ] Test `preferences.py` palette and cascade tables (only the core preference round-trip is covered).
- [ ] Verify the platformdirs paths on Windows in CI (add a `windows-latest` matrix leg once Tk-on-Windows CI is proven stable).
- [ ] Add a smoke test that launches the GUI under `xvfb` and closes it, to catch import-time widget regressions.

## Type & lint debt

- [ ] Bring the `view/` package under mypy incrementally (currently excluded). Start with `view_utils.py` and `about.py`.
- [ ] Replace remaining implicit-`Optional` defaults (`param=None` with non-optional annotations) flagged by mypy in `control_panel.py`.

## Refactors (bigger, tracked in IDEA.md)

- [ ] Split `view/control_panel.py` (~2575 lines) into panel + menu + palette modules.
- [ ] Split `demo/app.py` (~2000 lines) into per-tab modules.
- [ ] Investigate the CustomTkinter 5.2.2 `TclError` in widget `_draw` callbacks on Python 3.13.

## Packaging & docs

- [ ] Add a PyInstaller `build.sh` target for a standalone desktop app.
- [ ] Give the legacy `docs/UserGuide-*.md` pages Just-the-Docs front matter so they appear in the nav.
- [ ] Publish the docs site via GitHub Pages once CI is green.
