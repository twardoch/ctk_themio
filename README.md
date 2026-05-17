# ctk_themio

Visual theme editor for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). Design a theme, see it immediately on every widget type, save it as JSON.

## What CustomTkinter theming is

CustomTkinter is a modern Python GUI library that wraps Tkinter with a cleaner look and dark mode support. Its appearance is controlled by JSON theme files: a set of color and geometry values for each widget type, specified separately for light and dark mode.

A theme file looks like this:

```json
{
  "CTkButton": {
    "fg_color": ["#3B8ED0", "#1F6AA5"],
    "hover_color": ["#36719F", "#144870"],
    "border_color": ["#3E454A", "#949A9F"],
    "border_width": 0,
    "corner_radius": 6
  }
}
```

The first value in each pair is the light-mode color; the second is the dark-mode color. There are 18+ widget types, each with multiple color and geometry properties. Editing this by hand is tedious and hard to visualise.

## What ctk_themio does

It gives you a panel with color pickers and sliders on the left and a live preview panel showing all 18+ widgets on the right. Change a color; the preview updates immediately. Export the JSON when you are happy.

Additional features:

- **Color harmonics**: generate complementary, analogous, or triadic palettes from a base color
- **Theme merging**: combine properties from two theme files
- **Import/export**: load any existing CustomTkinter JSON theme for editing
- **Undo/redo**: full command stack for non-destructive editing
- **Geometry editing**: adjust corner radii and border widths with sliders

## Install

Requires Python 3.13+.

```bash
pip install ctk_themio
# or
uv pip install ctk_themio
```

### macOS / Linux

```bash
curl -LsSf uvx.sh/ctk_themio/install.sh | sh && ctk-themio
```

## Run

```bash
# Open the full theme editor
ctk-themio

# Open in preview-only mode with a specific appearance and theme
ctk-themio -a Dark -t my_theme.json

# Run the widget showcase demo
ctk-themio-demo
```

## Theme file format

Themes are JSON files stored in `~/.local/share/ctk_themio/themes/` (Linux), `~/Library/Application Support/ctk_themio/themes/` (macOS), or the equivalent Windows path. The built-in themes live inside the package and are copied to the user directory on first run.

Color values are `[light, dark]` pairs (hex strings). Geometry values are numbers. Both are stored in the same file and can be edited independently.

## Architecture

The application follows an MVC pattern:

- **Controller** (`controller/ctk_theme_builder.py`): parses CLI args, launches the correct window
- **Model** (`model/ctk_theme_builder.py`): theme loading/saving, undo/redo command stack, property change tracking
- **View** (`view/`): control panel (~2500 lines), live preview panel (~1300 lines), and a set of dialogs for harmonics, geometry, preferences, and merging
- **Utils** (`utils/cbtk_kit.py`): color manipulation — hex/RGB conversion, lightness adjustment, contrast checking

User preferences are stored in a SQLite database (auto-initialized on first run) via `model/preferences.py`. This tracks last-used theme, appearance mode, window geometry, and saved color palettes.

## Based on

`ctk_themio` is a repackaged and updated version of [CTk Theme Builder](https://github.com/avalon60/ctk_theme_builder) by Clive Bostock, published under MIT license.

## License

MIT
