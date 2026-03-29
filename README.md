# CTk Theme Builder (`ctk_themio`)

Visual theme editor for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) applications. Design, preview, and manage custom themes with a WYSIWYG interface.

<figure>
  <img src="docs/CTkThemeBuilder-about.png" alt="CTk Theme Builder" style="width:100%">
</figure>

## Installation

Requires **Python 3.13+**.

```bash
# From PyPI
pip install ctk_themio

# Or with uv
uv pip install ctk_themio

# Or via uvx (no install needed)
uvx ctk_themio
```

### From source

```bash
git clone https://github.com/twardoch/ctk_themio.git
cd ctk_themio
uv pip install -e .
```

## Usage

```bash
# Launch the theme editor
ctk-themio

# Launch in preview-only mode with a specific theme
ctk-themio -a Dark -t path/to/theme.json

# Run as a Python module
python -m ctk_themio

# Launch the widget demo showcase
ctk-themio-demo
```

### Command-line options

| Option | Description |
|--------|-------------|
| `-a`, `--set-appearance` | Set appearance mode: `Dark` or `Light` (default: `Dark`) |
| `-t`, `--set-theme` | Path to a theme JSON file. Launches preview-only mode. |

## Features

### Visual Theme Editing

Make changes and see the effects instantly across all 18+ CustomTkinter widget types. The live preview panel updates as you adjust colors, borders, corner radii, and spacing.

Supported widgets: CTk, CTkToplevel, CTkFrame, CTkScrollableFrame, CTkButton, CTkLabel, CTkEntry, CTkComboBox, CTkOptionMenu, CTkSlider, CTkProgressBar, CTkCheckBox, CTkRadioButton, CTkSwitch, CTkSegmentedButton, CTkTabview, CTkScrollbar, CTkTextbox, DropdownMenu.

### Light and Dark Modes

Every theme property supports dual values for light and dark appearance modes. Switch between modes instantly to verify your theme works in both contexts. A "render as disabled" mode lets you preview how widgets look when disabled.

### Color Tools

- **Color Palettes**: Associate a palette with each theme for quick access to your chosen colors. Copy and paste colors between elements with single-click paste mode.
- **Color Harmonics**: Generate complementary, analogous, triadic, and other color schemes from a base color using the Harmonics dialog.
- **Shade Adjustment**: Fine-tune color shades with configurable differential steps.
- **Auto Contrast**: Automatically adjust text colors for readability against their background.
- **Color Cascade**: Apply a palette color to multiple related widget properties at once.

### Widget Geometry

Edit borders, corner radii, button lengths, and spacing through the dedicated Geometry dialog. Changes propagate to the live preview immediately.

### Theme Management

- **Merge and Swap**: Combine elements from different themes or swap color palettes between themes.
- **Provenance**: Track theme metadata including author, creation date, modification date, and notes.
- **Import/Export**: Import themes from and export themes to JSON files.
- **Built-in Themes**: Ships with 14 ready-to-use themes: Anthracite, Blue, DaynNight, GhostTrain, Green, Greengage, GreyGhost, Hades, Harlequin, MoonlitSky, NightTrain, Oceanix, TrojanBlue, and more.

### User Preferences

Preferences persist across sessions via SQLite. Configurable options include:
- Auto-load last theme on start
- Enable/disable tooltips
- Widget scaling per panel (Control Panel, Preview, QA)
- Logging level and format
- Network listener port for QA testing

## Theme Format

Themes are JSON files mirroring the CustomTkinter widget property structure:

```json
{
  "CTkButton": {
    "fg_color": ["#3B8ED0", "#1F6AA5"],
    "hover_color": ["#36719F", "#144870"],
    "border_color": ["#3E454A", "#949A9F"],
    "text_color": ["#DCE4EE", "#DCE4EE"],
    "text_color_disabled": ["gray74", "gray60"],
    "corner_radius": 6,
    "border_width": 0
  }
}
```

Color values can be `[light_mode, dark_mode]` pairs or single values. Properties are split into color properties (fg_color, bg_color, hover_color, text_color, etc.) and geometry properties (border_width, corner_radius, button_length, etc.).

## Data Locations

User data is stored in OS-appropriate directories via [platformdirs](https://pypi.org/project/platformdirs/):

| Data | macOS | Linux | Windows |
|------|-------|-------|---------|
| Database, palettes, user themes | `~/Library/Application Support/ctk_themio/` | `~/.local/share/ctk_themio/` | `%LOCALAPPDATA%\twardoch\ctk_themio` |
| Logs | `~/Library/Logs/ctk_themio/` | `~/.local/state/ctk_themio/log/` | `%LOCALAPPDATA%\twardoch\ctk_themio\Logs` |
| Cache/temp | `~/Library/Caches/ctk_themio/` | `~/.cache/ctk_themio/` | `%LOCALAPPDATA%\twardoch\ctk_themio\Cache` |

On first run, bundled sample themes are copied to the user themes directory.

## Architecture

The application follows the **MVC pattern**:

- **`controller/`** - Entry point with CLI argument parsing. Launches the editor or preview-only mode.
- **`model/`** - Core business logic: theme loading/saving, undo/redo (`CommandStack`), preferences database (SQLite), color operations.
- **`view/`** - GUI components: main control panel, live preview panel, and dialogs for color harmonics, geometry editing, preferences, import/export, theme merging, and provenance.
- **`utils/`** - Color utilities (hex/rgb conversion, shading, contrast calculations), named color constants, logging.
- **`assets/`** - Bundled read-only data: built-in themes, view schemas, configuration, images.
- **`demo/`** - Widget showcase application with 13 interactive tabs.
- **`paths.py`** - Centralized path definitions using platformdirs.

## Development

```bash
# Clone and install in development mode
git clone https://github.com/twardoch/ctk_themio.git
cd ctk_themio
uv pip install -e .

# Build wheel and sdist
uvx hatch build

# Publish to PyPI
./publish.sh
```

### Build System

- **Build backend**: [hatchling](https://hatch.pypa.io/) with [hatch-vcs](https://github.com/ofek/hatch-vcs) for version management
- **Version**: Derived from git tags (semantic versioning)
- **Package layout**: `src/ctk_themio/` (standard src layout)

### Dependencies

| Package | Purpose |
|---------|---------|
| `customtkinter` | Modern Tkinter GUI framework |
| `colorharmonies` | Color harmony/scheme generation |
| `loguru` | Structured logging |
| `matplotlib` | Color utilities and validation |
| `pillow` | Image handling |
| `pyperclip` | Clipboard operations |
| `platformdirs` | OS-appropriate data directories |
| `CTkMessagebox` | Message dialog widget |
| `CTkToolTip` | Tooltip widget |
| `darkdetect` | OS dark mode detection |
| `fonttools` | Font manipulation |
| `pathvalidate` | Path validation |
| `numpy` | Numerical operations (matplotlib dependency) |
| `colour` | Color parsing |

## Credits

Originally created by **Clive Bostock**. Now maintained by **Adam Twardoch**.

Thanks to Tom Schimansky for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), and to Akash Bora for [CTkToolTip](https://github.com/Akascape/CTkToolTip) and [CTkMessagebox](https://github.com/Akascape/CTkMessagebox).

## License

[MIT](LICENSE)
