---
title: Home
layout: default
nav_order: 1
---

# ctk_themio

Design a CustomTkinter theme, watch it land on every widget the moment you change a colour, and save it as a JSON file your app can load unchanged.

CustomTkinter controls its look through JSON theme files: a light value and a dark value for each colour, plus geometry numbers like corner radius and border width. Editing that JSON by hand means guessing, saving, launching your app, squinting, and going back. `ctk_themio` closes that loop — a live preview panel shows all 18+ widget types at once, in the appearance mode you are editing.

![The three panels: controls, properties, live preview](3-panels.png)

## Install

```bash
uv tool install ctk_themio      # or: pipx install ctk_themio
ctk-themio
```

## Run

```bash
ctk-themio                       # full editor
ctk-themio -a Dark -t theme.json # preview a theme in dark mode, read-only
ctk-themio-demo                  # widget showcase
```

## Where to go next

- [Theme schema](theme-schema.md) — every colour and geometry key, and how light/dark pairs work.
- [User guide](CTkThemeBuilderUserGuide-3.1.md) — the full walkthrough: palettes, harmonics, cascades, merging.
- [Installs and upgrades](installs-upgrades.md) — packaging notes.

## Based on

`ctk_themio` is a repackaged, modernised fork of [CTk Theme Builder](https://github.com/avalon60/ctk_theme_builder) by Clive Bostock, MIT-licensed.
