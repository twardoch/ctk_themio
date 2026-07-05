---
title: Theme schema
layout: default
nav_order: 2
---

# Theme schema

A CustomTkinter theme is a single JSON object. Each top-level key is a widget type; its value is an object of properties. `ctk_themio` reads and writes exactly this shape, so anything you save loads straight into `customtkinter.set_default_color_theme()`.

## Light and dark, side by side

Every colour is a two-element array: light mode first, dark mode second.

```json
"CTkButton": {
  "fg_color": ["#3B8ED0", "#1F6AA5"],
  "hover_color": ["#36719F", "#144870"]
}
```

The editor shows one mode at a time. Switching the appearance toggle changes which element of each pair you are editing; both are stored in the same file.

Geometry properties are plain numbers, not pairs — they do not change between light and dark:

```json
"CTkButton": {
  "corner_radius": 6,
  "border_width": 0
}
```

A property value of `"transparent"` is legal for foreground colours and renders as the parent's background.

## Widget types

A complete theme carries an entry for each widget CustomTkinter can style:

| Group | Keys |
|-------|------|
| Windows | `CTk`, `CTkToplevel` |
| Containers | `CTkFrame`, `CTkScrollableFrame` |
| Buttons | `CTkButton`, `CTkSegmentedButton` |
| Inputs | `CTkEntry`, `CTkTextbox`, `CTkComboBox`, `CTkOptionMenu` |
| Toggles | `CTkCheckBox`, `CTkRadioButton`, `CTkSwitch` |
| Ranges | `CTkSlider`, `CTkProgressBar` |
| Chrome | `CTkScrollbar`, `DropdownMenu`, `CTkLabel` |
| Typography | `CTkFont` |

Widget names are case-sensitive and match CustomTkinter exactly — `CTkCheckBox` and `CTkRadioButton` carry a capital second word. (The bundled v4→v5 migrator, `utils/ctk_theme_migrate.py`, honours this; an older casing bug that crashed conversion is fixed.)

## Colour versus geometry

Two kinds of property share each widget block:

- **Colour** — `fg_color`, `bg_color`, `hover_color`, `border_color`, `text_color`, `progress_color`, and their siblings. Edited in the properties panel's colour view.
- **Geometry** — `corner_radius`, `border_width`, `border_spacing`, and the widget-specific spacings. Edited in the geometry view.

Which properties appear for a given widget is driven by the view schemas in `assets/views/` — `Basic.json` and `Categorised.json` map each widget to the properties worth showing.

## Starting points

- `assets/etc/theme_skeleton.json` — a full, empty template with every widget key present. New themes begin here.
- `assets/themes/` and the bundled `user_themes/` — 14+ worked examples you can open, tweak, and save under a new name.
