# this_file: tests/test_cbtk_kit.py
"""Headless tests for the colour and geometry helpers in ``cbtk_kit``.

None of these touch a display: they exercise the pure maths that turns a hex
string into a lighter, darker, or contrasting colour, plus the small geometry
and text utilities the GUI leans on.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ctk_themio.utils import cbtk_kit

THEMES_DIR = Path(cbtk_kit.__file__).resolve().parent.parent / "user_themes"


def test_hex2rgb_parses_channels() -> None:
    assert cbtk_kit.hex2rgb("#3B8ED0") == (59, 142, 208)
    # A leading '#' is optional.
    assert cbtk_kit.hex2rgb("1F6AA5") == (31, 106, 165)


def test_rgb2hex_roundtrips() -> None:
    for colour in ("#000000", "#ffffff", "#3b8ed0", "#1f6aa5"):
        assert cbtk_kit.rgb2hex(cbtk_kit.hex2rgb(colour)) == colour


def test_shade_up_lightens() -> None:
    lighter = cbtk_kit.shade_up("#101010", differential=20)
    assert cbtk_kit.hex2rgb(lighter) == (36, 36, 36)


def test_shade_down_darkens() -> None:
    darker = cbtk_kit.shade_down("#303030", differential=20)
    assert cbtk_kit.hex2rgb(darker) == (28, 28, 28)


def test_shade_up_refuses_to_overflow() -> None:
    # Near-white cannot get lighter without skewing the balance, so it is left
    # untouched rather than clipped unevenly.
    assert cbtk_kit.shade_up("#f5f5f5", differential=40) == "#f5f5f5"


def test_shade_down_refuses_to_underflow() -> None:
    assert cbtk_kit.shade_down("#0a0a0a", differential=40) == "#0a0a0a"


@pytest.mark.parametrize("fn", [cbtk_kit.shade_up, cbtk_kit.shade_down, cbtk_kit.contrast_colour])
def test_transparent_none_returns_grey(fn) -> None:
    # A "transparent" property arrives as None; the helpers fall back to grey.
    assert fn(None) == "#b0b0b0"


def test_contrast_colour_moves_away_from_source() -> None:
    assert cbtk_kit.contrast_colour("#000000", differential=20) == "#141414"
    assert cbtk_kit.contrast_colour("#ffffff", differential=20) == "#ebebeb"


def test_str_mode_to_int() -> None:
    assert cbtk_kit.str_mode_to_int("Light") == 0
    assert cbtk_kit.str_mode_to_int("dark") == 1


def test_geometry_offset_adds_increments() -> None:
    assert cbtk_kit.geometry_offset("300x400+100+50", 30, 20) == "+130+70"


def test_geometry_offset_handles_empty() -> None:
    assert cbtk_kit.geometry_offset("") == "+0+0"
    assert cbtk_kit.geometry_offset(None) == "+0+0"


def test_geometry_offset_rejects_negative() -> None:
    # A genuine negative screen position is unsupported and collapses to the
    # origin; a "+-" artifact from Tk is normalised to its positive form.
    assert cbtk_kit.geometry_offset("300x400-10+50") == "+0+0"
    assert cbtk_kit.geometry_offset("300x400+-10+50") == "+10+50"


def test_wrap_string_breaks_on_width() -> None:
    wrapped = cbtk_kit.wrap_string("one two three four", wrap_width=8)
    assert wrapped.endswith("\n")
    assert all(len(line) <= 8 for line in wrapped.splitlines())


def test_theme_property_reads_bundled_theme() -> None:
    theme = THEMES_DIR / "Blue.json"
    light = cbtk_kit.theme_property_color(theme, "CTkButton", "fg_color", "light")
    dark = cbtk_kit.theme_property_color(theme, "CTkButton", "fg_color", "dark")
    assert light.startswith("#") and dark.startswith("#")
    assert light != dark
