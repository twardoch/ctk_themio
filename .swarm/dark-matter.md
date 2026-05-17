## Dark Matter: Hidden Couplings

Found 20 file pairs that frequently co-change but have no import relationship:

| File A | File B | NPMI | Co-Changes | Lift |
|--------|--------|------|------------|------|
| utils/freeze.sh | utils/tb-package.sh | 1.000 | 3 | 140.67 |
| view/harmonics_dialog.py | view/theme_merger.py | 1.000 | 3 | 140.67 |
| assets/themes/GreyGhost.json | assets/themes/MoonlitSky.json | 1.000 | 3 | 140.67 |
| assets/themes/GreyGhost.json | assets/themes/NightTrain.json | 1.000 | 3 | 140.67 |
| assets/themes/MoonlitSky.json | assets/themes/NightTrain.json | 1.000 | 3 | 140.67 |
| view/ctk_theme_preview.py | view/geometry_dialog.py | 0.942 | 3 | 105.50 |
| view/geometry_dialog.py | view/harmonics_dialog.py | 0.942 | 3 | 105.50 |
| view/geometry_dialog.py | view/theme_merger.py | 0.942 | 3 | 105.50 |
| assets/themes/GreyGhost.json | assets/themes/TrojanBlue.json | 0.942 | 3 | 105.50 |
| assets/themes/MoonlitSky.json | assets/themes/TrojanBlue.json | 0.942 | 3 | 105.50 |
| assets/themes/NightTrain.json | assets/themes/TrojanBlue.json | 0.942 | 3 | 105.50 |
| user_themes/MoonlitSky.json | user_themes/NightTrain.json | 0.924 | 5 | 60.29 |
| user_themes/GhostTrain.json | user_themes/MoonlitSky.json | 0.880 | 4 | 60.29 |
| user_themes/GhostTrain.json | user_themes/TrojanBlue.json | 0.851 | 4 | 52.75 |
| user_themes/GhostTrain.json | user_themes/GreyGhost.json | 0.839 | 3 | 63.30 |
| user_themes/GhostTrain.json | user_themes/NightTrain.json | 0.839 | 3 | 63.30 |
| user_themes/GreyGhost.json | user_themes/MoonlitSky.json | 0.832 | 4 | 48.23 |
| lib/about.py | lib/control_panel.py | 0.829 | 3 | 60.29 |
| docs/harmonics.md | docs/menus.md | 0.818 | 5 | 37.68 |
| user_themes/GhostTrain.json | user_themes/Oceanix.json | 0.803 | 4 | 42.20 |

These pairs likely share an architectural concern invisible to static analysis.
Consider adding explicit documentation or extracting the shared concern.