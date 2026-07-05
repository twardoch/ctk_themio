# this_file: tests/test_migrate.py
"""Functional test for the v4 -> v5 theme migrator.

We feed a complete CustomTkinter v4 colour block through ``ThemeConverter`` and
confirm the v5 output is valid JSON with the colours mapped onto the right
widgets. The module also has to import without running its CLI.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

from ctk_themio import paths
from ctk_themio.utils.ctk_theme_migrate import ThemeConverter

# Every colour key that convert_json() reads from the v4 theme.
_V4_COLOUR_KEYS = [
    "window_bg_color",
    "frame_low",
    "frame_high",
    "frame_border",
    "button",
    "button_hover",
    "button_border",
    "text",
    "text_disabled",
    "entry",
    "entry_border",
    "entry_placeholder_text",
    "checkbox_border",
    "checkmark",
    "switch",
    "switch_progress",
    "switch_button",
    "switch_button_hover",
    "progressbar",
    "progressbar_progress",
    "progressbar_border",
    "slider",
    "slider_progress",
    "dropdown_color",
    "optionmenu_button",
    "optionmenu_button_hover",
    "dropdown_text",
    "combobox_border",
    "combobox_button_hover",
    "scrollbar_button",
    "scrollbar_button_hover",
    "dropdown_hover",
]


def test_module_imports_without_running_cli() -> None:
    # A regression guard: the migrator used to parse argv at import time and
    # crash. Re-importing it must stay side-effect free.
    module = importlib.import_module("ctk_themio.utils.ctk_theme_migrate")
    assert hasattr(module, "main")
    assert callable(module.main)


def test_v4_to_v5_conversion(tmp_path: Path) -> None:
    v4 = {"color": {key: "#123456" for key in _V4_COLOUR_KEYS}}
    v4["color"]["button"] = "#3b8ed0"
    in_file = tmp_path / "v4.json"
    out_file = tmp_path / "v5.json"
    in_file.write_text(json.dumps(v4))

    converter = ThemeConverter(
        application_home=paths.PKG_DIR,
        theme_file_in=in_file,
        theme_file_out=out_file,
        strict=False,
    )
    converter.load_theme()
    converter.convert_json()
    converter.dump_theme()

    assert out_file.exists()
    v5 = json.loads(out_file.read_text())
    # The v4 "button" colour must land on the v5 CTkButton foreground.
    assert v5["CTkButton"]["fg_color"] == "#3b8ed0"
    # Non-strict mode substitutes frame_low for the window background.
    assert v5["CTk"]["fg_color"] == v4["color"]["frame_low"]
