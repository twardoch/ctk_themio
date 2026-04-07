# this_file: src/ctk_themio/__main__.py
"""
Entry point for python -m execution.

Allows running the CTk Theme Builder application as a Python module:
`python -m ctk_themio`

This is an alternative to the `ctk-themio` console script.
"""

from ctk_themio.controller.ctk_theme_builder import main

if __name__ == "__main__":
    main()
