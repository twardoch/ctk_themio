# this_file: src/ctk_themio/demo/app.py
from __future__ import annotations

import asyncio
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from typing import Any
import json

try:
    import customtkinter as ctk  # type: ignore[import-untyped]
except ImportError as exc:
    raise SystemExit(f"[fatal] customtkinter is required: {exc}") from exc


def warn_import(name: str, exc: Exception) -> None:  # noqa: ARG001
    pass


try:
    from ctk_components import CTkCarousel, CTkLoader, CTkPopupMenu, CTkProgressPopup, do_popup  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("ctkcomponents", exc)
    CTkCarousel = CTkLoader = CTkPopupMenu = CTkProgressPopup = None  # type: ignore[assignment]
    do_popup = None  # type: ignore[assignment]

try:
    from CTkMenuBarPlus import CTkMenuBar, CustomDropdownMenu, ContextMenu  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("CTkMenuBarPlus", exc)
    CTkMenuBar = CustomDropdownMenu = ContextMenu = None  # type: ignore[assignment]

try:
    from CTkToolTip import CTkToolTip  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("CTkToolTip", exc)
    CTkToolTip = None  # type: ignore[assignment]

try:
    from MoreCustomTkinterWidgets import Separator, BetterCTkImage  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("MoreCustomTkinterWidgets", exc)
    Separator = BetterCTkImage = None  # type: ignore[assignment]

try:
    from CTkScrollableDropdownPP import CTkScrollableDropdown  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("CTkScrollableDropdownPP", exc)
    CTkScrollableDropdown = None  # type: ignore[assignment]

try:
    from ctk_listbox import CTkListbox  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("ctk-listbox-typed", exc)
    CTkListbox = None  # type: ignore[assignment]

try:
    from tkinter_videoplayer import VideoPlayer  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("tkinter-videoplayer", exc)
    VideoPlayer = None  # type: ignore[assignment]

try:
    from ctksidebar import CTkSidebarNavigation  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("ctk-sidebar", exc)
    CTkSidebarNavigation = None  # type: ignore[assignment]

try:
    from ctk_toggle import CTkToggleButton, CTkToggleGroup  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("ctk-toggle", exc)
    CTkToggleButton = CTkToggleGroup = None  # type: ignore[assignment]

try:
    from tkinterweb import HtmlFrame  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("tkinterweb", exc)
    HtmlFrame = None  # type: ignore[assignment]

try:
    from tkinter_layout_helpers.grid_helper import grid_manager  # type: ignore[import-untyped]
    from tkinter_layout_helpers import pack_manager  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("tkinter-layout-helpers", exc)
    grid_manager = pack_manager = None  # type: ignore[assignment]

try:
    import tkinter_kit.func as tkk  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("tkinter-kit", exc)
    tkk = None  # type: ignore[assignment]


try:
    import tkinter_page as tkp  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("tkinter-page", exc)
    tkp = None  # type: ignore[assignment]

try:
    from tktooltip import ToolTip  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("tkinter-tooltip", exc)
    ToolTip = None  # type: ignore[assignment]

try:
    from async_tkinter_loop import async_handler, async_mainloop  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("async-tkinter-loop", exc)

    def async_handler(func: Any) -> Any:  # noqa: ARG001
        """Fallback: disable async buttons when async-tkinter-loop is missing."""

        def _noop(*_args: Any, **_kwargs: Any) -> None:
            pass

        return _noop

    async_mainloop = None  # type: ignore[assignment]

try:
    import tk_async_execute as tae  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("tkinter-async-execute", exc)
    tae = None  # type: ignore[assignment]

try:
    from PIL import Image, ImageDraw  # type: ignore[import-untyped]
except ImportError as exc:
    raise SystemExit(f"[fatal] Pillow is required: {exc}") from exc

try:
    from ttkbootstrap_icons_bs import BootstrapIcon  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("ttkbootstrap-icons-bs", exc)
    BootstrapIcon = None  # type: ignore[assignment]

try:
    from tklive import live as tklive_live  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("tklive", exc)
    tklive_live = None  # type: ignore[assignment]

try:
    from ttk_text import ThemedText  # type: ignore[import-untyped]
    from ttk_text.scrolled_text import ScrolledText as TtkScrolledText  # type: ignore[import-untyped]
except ImportError as exc:
    warn_import("ttk-text", exc)
    ThemedText = TtkScrolledText = None  # type: ignore[assignment]

def replace_theme_colors(d, replacements):
    """Recursively replace color values in a customtkinter theme dict in-place.
    
    replacements: dict mapping old_color -> new_color (case-insensitive matching)
    """
    lower_map = {k.lower(): v for k, v in replacements.items()}
    for key, val in d.items():
        if isinstance(val, dict):
            replace_theme_colors(val, replacements)
        elif isinstance(val, list):
            for i, item in enumerate(val):
                if isinstance(item, str) and item.lower() in lower_map:
                    val[i] = lower_map[item.lower()]
        elif isinstance(val, str) and val.lower() in lower_map:
            d[key] = lower_map[val.lower()]





TAB_NAMES: list[str] = [
    "Core Widgets",
    "Dropdowns & Lists",
    "Containers",
    "Toggles & Groups",
    "Carousel & Loader",
    "Progress & Popups",
    "HTML Viewer",
    "Media Player",
    "Layout Helpers",
    "Async Demo",
    "Icons (Bootstrap)",
    "Themed Text",
    "Dev Tools",
]

DATA_DIR = Path(__file__).parent / "data"


class InlineLoaderOverlay:
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self._after_id: str | None = None
        self._dot_phase = 0

        self.frame = ctk.CTkFrame(master, corner_radius=0, fg_color=("#dfe3eb", "#171a20"))
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.panel = ctk.CTkFrame(self.frame, width=260, height=120, corner_radius=12)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")
        self.panel.pack_propagate(False)

        self.label = ctk.CTkLabel(self.panel, text="Loading", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(pady=(26, 8))

        self.progress = ctk.CTkProgressBar(self.panel, mode="indeterminate", width=180)
        self.progress.pack(pady=(0, 22))
        self.progress.start()

        self._animate()

    def _animate(self) -> None:
        if not self.frame.winfo_exists():
            return
        dots = "." * ((self._dot_phase % 3) + 1)
        self.label.configure(text=f"Loading{dots}")
        self._dot_phase += 1
        self._after_id = self.frame.after(260, self._animate)

    def stop_loader(self) -> None:
        if self._after_id is not None:
            self.frame.after_cancel(self._after_id)
            self._after_id = None
        try:
            self.progress.stop()
        except Exception:
            pass
        if self.frame.winfo_exists():
            self.frame.destroy()


class InlineProgressPopup:
    def __init__(
        self,
        master: ctk.CTk,
        title: str,
        label: str,
        message: str,
        side: str = "right_bottom",  # noqa: ARG002
    ) -> None:
        self.master = master
        self.window = ctk.CTkToplevel(master)
        self.window.title(title)
        self.window.resizable(False, False)

        self.master.update_idletasks()
        popup_width, popup_height = 340, 140
        pos_x = self.master.winfo_rootx() + self.master.winfo_width() - popup_width - 20
        pos_y = self.master.winfo_rooty() + self.master.winfo_height() - popup_height - 48
        self.window.geometry(f"{popup_width}x{popup_height}+{max(pos_x, 20)}+{max(pos_y, 20)}")
        self.window.transient(master)
        self.window.attributes("-topmost", True)
        self.window.after(300, lambda: self.window.attributes("-topmost", False))

        shell = ctk.CTkFrame(self.window, corner_radius=10)
        shell.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.title_label = ctk.CTkLabel(shell, text=label, font=ctk.CTkFont(size=14, weight="bold"))
        self.title_label.pack(anchor="w", padx=10, pady=(8, 2))

        self.message_label = ctk.CTkLabel(shell, text=message)
        self.message_label.pack(anchor="w", padx=10, pady=(0, 8))

        self.progress = ctk.CTkProgressBar(shell)
        self.progress.set(0.0)
        self.progress.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.window.protocol("WM_DELETE_WINDOW", self.close_progress_popup)

    def update_progress(self, value: float) -> None:
        self.progress.set(max(0.0, min(value, 1.0)))

    def update_message(self, message: str) -> None:
        self.message_label.configure(text=message)

    def close_progress_popup(self) -> None:
        if self.window.winfo_exists():
            self.window.destroy()


class CtkMegaDemo(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=("#f8f8fa", "#17171a"))
        self.title("CustomTkinter: Full Widget + Extensions Demo")
        self.geometry("1320x860")
        self.minsize(1200, 800)

        self.context_menu: Any = None
        self._appearance_checks: dict[str, Any] = {}
        self._demo_disabled_option: Any = None
        self._recent_menu: Any = None
        self._recent_option_items: list[Any] = []
        self.loader_overlay: Any = None
        self.progress_popup: Any = None
        self.progress_value = 0.0
        self.carousel_images: list[ctk.CTkImage] = []
        self.carousel_index = 0
        self.carousel_after_id: str | None = None
        self.video_player: VideoPlayer | None = None
        self.tae_running = False
        self._closing = False

        self.radio_var = tk.StringVar(value="A")
        self.switch_var = tk.BooleanVar(value=True)
        self.checkbox_var = tk.BooleanVar(value=False)
        self.slider_var = tk.DoubleVar(value=35)
        self.progress_var = tk.DoubleVar(value=0.35)
        self.status_var = tk.StringVar(value="Ready")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._build_menu_bar()
        self._build_layout_shell()
        self._build_tabs()
        self._build_bottom_status_bar()
        self._install_global_popup()

        if tae is not None:
            try:
                tae.start()
                self.tae_running = True
                self.set_status("tkinter_async_execute started")
            except Exception as exc:
                warn_import("tkinter_async_execute.start", exc)
                self.tae_running = False

        self.after(50, self._raise_window)

    def _raise_window(self) -> None:
        self.lift()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))
        self.focus_force()

    def set_status(self, text: str) -> None:
        if self._closing:
            return
        self.status_var.set(text)

    def _build_menu_bar(self) -> None:
        if CTkMenuBar is None or CustomDropdownMenu is None:
            fallback = ctk.CTkFrame(self, corner_radius=8)
            fallback.pack(fill=tk.X, padx=10, pady=(10, 6))
            ctk.CTkLabel(
                fallback,
                text="CTkMenuBar not available. Menus are disabled.",
                anchor="w",
            ).pack(fill=tk.X, padx=10, pady=8)
            return

        self.menu_bar = CTkMenuBar(self, bg_color=["#f8f8fa", "#17171a"])
        self.menu_bar.pack(fill=tk.X, padx=10, pady=(10, 4))

        # -- File menu -------------------------------------------------
        file_btn = self.menu_bar.add_cascade(text="File")
        ui_font = file_btn.cget("font")
        file_menu = CustomDropdownMenu(widget=file_btn, width=200, font=ui_font)
        file_menu.add_option(
            option="New Project",
            command=lambda: self.set_status("New project created"),
            accelerator="CmdOrCtrl+N",
        )
        file_menu.add_option(
            option="Open Input Dialog",
            command=self.show_input_dialog,
            accelerator="CmdOrCtrl+O",
        )
        file_menu.add_option(
            option="Open Toplevel",
            command=self.open_toplevel_demo,
            accelerator="CmdOrCtrl+T",
        )
        file_menu.add_separator()
        export_sub = file_menu.add_submenu("Export As", accelerator="CmdOrCtrl+E")
        export_sub.add_option(
            option="PDF",
            command=lambda: self.set_status("Export requested: PDF"),
            accelerator="CmdOrCtrl+Shift+P",
        )
        export_sub.add_option(
            option="SVG",
            command=lambda: self.set_status("Export requested: SVG"),
            accelerator="CmdOrCtrl+Shift+S",
        )
        export_sub.add_option(
            option="PNG",
            command=lambda: self.set_status("Export requested: PNG"),
            accelerator="CmdOrCtrl+Shift+G",
        )
        file_menu.add_separator()
        self._recent_menu = file_menu.add_submenu("Recent Files", max_visible_options=5)
        self._recent_option_items = []
        self._seed_recent_items()
        self._recent_menu.add_separator()
        self._recent_menu.add_option(
            option="Clear Recent",
            command=self._clear_recent_items,
        )
        self._recent_menu.add_option(
            option="Reset Recent (clean demo)",
            command=self._reset_recent_menu,
        )
        file_menu.add_separator()
        file_menu.add_option(option="Quit", command=self.on_close, accelerator="Alt+F4")

        # -- Edit menu -------------------------------------------------
        edit_btn = self.menu_bar.add_cascade(text="Edit")
        edit_menu = CustomDropdownMenu(widget=edit_btn, width=200, font=ui_font)
        edit_menu.add_option(
            option="Clear Status",
            command=lambda: self.set_status("Ready"),
            accelerator="CmdOrCtrl+K",
        )
        edit_menu.add_option(
            option="Progress Popup",
            command=self.start_progress_popup,
            accelerator="CmdOrCtrl+P",
        )
        edit_menu.add_option(
            option="Toggle Loader",
            command=self.toggle_loader,
            accelerator="CmdOrCtrl+L",
        )
        edit_menu.add_separator()
        # Demonstrate enable/disable: a disabled item that gets enabled later
        self._demo_disabled_option = edit_menu.add_option(
            option="Locked Action (enable via Help)",
            command=lambda: self.set_status("Locked action triggered!"),
            enabled=False,
        )

        # -- View menu -------------------------------------------------
        view_btn = self.menu_bar.add_cascade(text="View")
        view_menu = CustomDropdownMenu(widget=view_btn, width=220, font=ui_font)
        # Checkable items for appearance mode
        self._appearance_checks = {}
        for mode in ("Dark", "Light", "System"):
            opt = view_menu.add_option(
                option=f"Appearance: {mode}",
                command=lambda m=mode: self._set_appearance_checked(m),
                accelerator=f"CmdOrCtrl+{mode[0]}",
                checkable=True,
                checked=(mode == "System"),
            )
            self._appearance_checks[mode] = opt
        view_menu.add_separator()
        view_menu.add_option(
            option="Reset Layout",
            command=lambda: self.set_status("Layout reset (demo)"),
            accelerator="CmdOrCtrl+Shift+R",
        )

        # -- Help menu (scrollable) -----------------------------------
        help_btn = self.menu_bar.add_cascade(text="Help")
        help_menu = CustomDropdownMenu(widget=help_btn, width=260, font=ui_font)
        help_menu.add_option(option="About ThemeManager", command=self.show_theme_info, accelerator="F1")
        help_menu.add_option(
            option="About Async",
            command=lambda: self.set_status("See Async Demo tab"),
        )
        help_menu.add_separator()
        # Scrollable submenu showcasing max_visible_options
        tips_sub = help_menu.add_submenu("Tips & Tricks", max_visible_options=5, accelerator="F2")
        for i in range(1, 11):
            tips_sub.add_option(
                option=f"Tip #{i}: Lorem ipsum tip number {i}",
                command=lambda n=i: self.set_status(f"Tip #{n} selected"),
            )
        help_menu.add_separator()
        help_menu.add_option(
            option="Enable Locked Action",
            command=self._enable_locked_action,
            accelerator="F3",
        )
        help_menu.add_option(
            option="Remove This Option (demo)",
            command=lambda: self._demo_remove_option(help_menu, "Remove This Option (demo)"),
        )

    def _set_appearance_checked(self, mode: str) -> None:
        """Switch appearance and update checkable menu items."""
        self.set_appearance(mode)
        for m, opt in self._appearance_checks.items():
            opt.set_checked(m == mode)

    def _enable_locked_action(self) -> None:
        """Enable the disabled demo option in the Edit menu."""
        if hasattr(self, "_demo_disabled_option") and self._demo_disabled_option is not None:
            self._demo_disabled_option.enable()
            self.set_status("Locked action is now enabled!")

    def _demo_remove_option(self, menu: Any, option_name: str) -> None:
        """Demonstrate remove_option by removing the calling item."""
        try:
            menu.remove_option(option_name)
            self.set_status(f"Removed menu option: {option_name}")
        except Exception:
            self.set_status("remove_option not available in this version")

    def _seed_recent_items(self) -> None:
        sample_files = [
            "project_alpha.lines",
            "wireframe_v2.lines",
            "icon_set_draft.lines",
            "logo_final.lines",
            "background_pattern.lines",
            "ui_mockup.lines",
            "banner_2026.lines",
        ]
        for name in sample_files:
            opt = self._recent_menu.add_option(
                option=name,
                command=lambda n=name: self.set_status(f"Open recent: {n}"),
            )
            self._recent_option_items.append((name, opt))

    def _clear_recent_items(self) -> None:
        for name, _opt in self._recent_option_items:
            try:
                self._recent_menu.remove_option(name)
            except Exception:
                pass
        self._recent_option_items.clear()
        self.set_status("Recent files cleared (remove_option demo)")

    def _reset_recent_menu(self) -> None:
        try:
            self._recent_menu.clean()
        except Exception:
            self.set_status("clean() not available in this version")
            return
        self._recent_option_items.clear()
        self._seed_recent_items()
        self._recent_menu.add_separator()
        self._recent_menu.add_option(
            option="Clear Recent",
            command=self._clear_recent_items,
        )
        self._recent_menu.add_option(
            option="Reset Recent (clean demo)",
            command=self._reset_recent_menu,
        )
        self.set_status("Recent menu reset (clean demo)")

    def _build_layout_shell(self) -> None:
        self.main_area = ctk.CTkFrame(self, corner_radius=12)
        self.main_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 6))

        self.sidebar_holder = ctk.CTkFrame(self.main_area, width=220, corner_radius=10)
        self.sidebar_holder.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 4), pady=8)
        self.sidebar_holder.pack_propagate(False)

        self.center_holder = ctk.CTkFrame(self.main_area, corner_radius=10)
        self.center_holder.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 8), pady=8)

        self.tabview = ctk.CTkTabview(self.center_holder, corner_radius=10)
        self.tabview.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        if CTkSidebarNavigation is not None:
            try:
                self.sidebar = CTkSidebarNavigation(self.sidebar_holder, width=200)
                for tab_name in TAB_NAMES:
                    tab_id = tab_name.lower().replace(" ", "_").replace("&", "and")
                    self.sidebar.sidebar.add_item(
                        id=tab_id,
                        text=tab_name,
                        command=lambda _id=None, name=tab_name: self.tabview.set(name),
                    )
                self.sidebar.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
            except Exception as exc:
                warn_import("CTkSidebarNavigation runtime", exc)
                self._build_sidebar_fallback()
        else:
            self._build_sidebar_fallback()

    def _build_sidebar_fallback(self) -> None:
        ctk.CTkLabel(self.sidebar_holder, text="Navigation", font=ctk.CTkFont(size=16, weight="bold")).pack(
            padx=8, pady=(10, 6)
        )
        button_frame = ctk.CTkScrollableFrame(self.sidebar_holder, corner_radius=8)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        for tab_name in TAB_NAMES:
            ctk.CTkButton(
                button_frame,
                text=tab_name,
                command=lambda name=tab_name: self.tabview.set(name),
            ).pack(fill=tk.X, pady=4)

    def _build_tabs(self) -> None:
        self.tabs: dict[str, ctk.CTkFrame] = {}
        for name in TAB_NAMES:
            self.tabs[name] = self.tabview.add(name)

        self.build_core_widgets_tab(self.tabs["Core Widgets"])
        self.build_dropdowns_lists_tab(self.tabs["Dropdowns & Lists"])
        self.build_containers_tab(self.tabs["Containers"])
        self.build_toggles_groups_tab(self.tabs["Toggles & Groups"])
        self.build_carousel_loader_tab(self.tabs["Carousel & Loader"])
        self.build_progress_popup_tab(self.tabs["Progress & Popups"])
        self.build_html_tab(self.tabs["HTML Viewer"])
        self.build_media_player_tab(self.tabs["Media Player"])
        self.build_layout_helpers_tab(self.tabs["Layout Helpers"])
        self.build_async_tab(self.tabs["Async Demo"])
        self.build_icons_tab(self.tabs["Icons (Bootstrap)"])
        self.build_themed_text_tab(self.tabs["Themed Text"])
        self.build_devtools_tab(self.tabs["Dev Tools"])

    def _build_bottom_status_bar(self) -> None:
        status_bar = ctk.CTkFrame(self, corner_radius=10)
        status_bar.pack(fill=tk.X, padx=10, pady=(0, 10))

        ctk.CTkLabel(status_bar, textvariable=self.status_var, anchor="w").pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(10, 8),
            pady=8,
        )

        self.appearance_segment = ctk.CTkSegmentedButton(
            status_bar,
            values=["Dark", "Light", "System"],
            command=self.set_appearance,
            width=260,
        )
        self.appearance_segment.pack(side=tk.RIGHT, padx=(6, 10), pady=8)
        self.appearance_segment.set("System")

    def _install_global_popup(self) -> None:
        if ContextMenu is None:
            self.set_status("ContextMenu unavailable (install CTkMenuBarPlus)")
            return

        try:
            self.context_menu = ContextMenu(widget=self, width=220, scale=0.9)
            self.context_menu.add_option(
                option="Open Input Dialog",
                command=self.show_input_dialog,
                accelerator="CmdOrCtrl+O",
            )
            self.context_menu.add_option(
                option="Start Progress Popup",
                command=self.start_progress_popup,
                accelerator="CmdOrCtrl+P",
            )
            self.context_menu.add_option(
                option="Toggle Loader",
                command=self.toggle_loader,
                accelerator="CmdOrCtrl+L",
            )
            self.context_menu.add_separator()
            clipboard_sub = self.context_menu.add_submenu("Clipboard")
            clipboard_sub.add_option(
                option="Cut",
                command=lambda: self.set_status("Cut (demo)"),
                accelerator="CmdOrCtrl+X",
            )
            clipboard_sub.add_option(
                option="Copy",
                command=lambda: self.set_status("Copy (demo)"),
                accelerator="CmdOrCtrl+C",
            )
            clipboard_sub.add_option(
                option="Paste",
                command=lambda: self.set_status("Paste (demo)"),
                accelerator="CmdOrCtrl+V",
            )
            self.context_menu.add_separator()
            self.context_menu.add_option(
                option="About",
                command=self.show_theme_info,
            )
            self.set_status("Right-click context menu enabled")
        except Exception as exc:
            warn_import("ContextMenu runtime", exc)

    def add_ctk_tooltip(self, widget: Any, message: str) -> None:
        if CTkToolTip is None:
            return
        try:
            CTkToolTip(
                widget,
                message=message,
                delay=0.2,
                follow=True,
                x_offset=20,
                y_offset=10,
                alpha=0.95,
            )
        except Exception as exc:
            warn_import("CTkToolTip runtime", exc)

    def add_tk_tooltip(self, widget: Any, message: str) -> None:
        if ToolTip is None:
            return
        try:
            ToolTip(widget, msg=message, delay=0.5, follow=True)
        except Exception as exc:
            warn_import("tktooltip runtime", exc)

    def build_core_widgets_tab(self, tab: ctk.CTkFrame) -> None:
        left = ctk.CTkFrame(tab, corner_radius=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        right = ctk.CTkFrame(tab, corner_radius=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)

        ctk.CTkLabel(
            left,
            text="Core Widgets",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=12, pady=(12, 8))

        self.core_label = ctk.CTkLabel(left, text="CTkLabel + CTkImage demo")
        self.core_label.pack(anchor="w", padx=12, pady=4)

        pil_light = Image.new("RGBA", (90, 42), color="#4d8ff8")
        draw_light = ImageDraw.Draw(pil_light)
        draw_light.rectangle((4, 4, 86, 38), outline="#ffffff", width=2)
        draw_light.text((22, 12), "CTk", fill="#ffffff")

        pil_dark = Image.new("RGBA", (90, 42), color="#122844")
        draw_dark = ImageDraw.Draw(pil_dark)
        draw_dark.rectangle((4, 4, 86, 38), outline="#86c6ff", width=2)
        draw_dark.text((19, 12), "Demo", fill="#86c6ff")

        self.core_ctk_image = ctk.CTkImage(light_image=pil_light, dark_image=pil_dark, size=(90, 42))
        image_holder = ctk.CTkLabel(left, text="", image=self.core_ctk_image)
        image_holder.pack(anchor="w", padx=12, pady=(2, 8))

        if BetterCTkImage is not None:
            try:
                self.better_img = BetterCTkImage(
                    light_image=pil_light,
                    dark_image=pil_dark,
                    size=(100, 50),
                    rounded_corner_radius=12,
                )
                ctk.CTkLabel(left, text="", image=self.better_img).pack(anchor="w", padx=12, pady=(0, 8))
            except Exception as exc:
                warn_import("BetterCTkImage runtime", exc)
                ctk.CTkLabel(left, text="[BetterCTkImage failed at runtime]").pack(anchor="w", padx=12, pady=(0, 8))
        else:
            ctk.CTkLabel(left, text="[BetterCTkImage unavailable]").pack(anchor="w", padx=12, pady=(0, 8))

        self.core_entry = ctk.CTkEntry(left, placeholder_text="CTkEntry input")
        self.core_entry.pack(fill=tk.X, padx=12, pady=4)

        self.core_textbox = ctk.CTkTextbox(left, height=120)
        self.core_textbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
        self.core_textbox.insert("1.0", "CTkTextbox\n- multiline\n- editable\n- selectable\n")

        controls = ctk.CTkFrame(right)
        controls.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.core_checkbox = ctk.CTkCheckBox(controls, text="CTkCheckBox", variable=self.checkbox_var)
        self.core_checkbox.pack(anchor="w", pady=5)

        self.core_radio_a = ctk.CTkRadioButton(
            controls,
            text="CTkRadioButton A",
            value="A",
            variable=self.radio_var,
        )
        self.core_radio_b = ctk.CTkRadioButton(
            controls,
            text="CTkRadioButton B",
            value="B",
            variable=self.radio_var,
        )
        self.core_radio_a.pack(anchor="w", pady=4)
        self.core_radio_b.pack(anchor="w", pady=4)

        self.core_switch = ctk.CTkSwitch(
            controls,
            text="CTkSwitch",
            variable=self.switch_var,
            command=lambda: self.set_status(f"Switch: {self.switch_var.get()}"),
        )
        self.core_switch.pack(anchor="w", pady=5)

        self.core_slider = ctk.CTkSlider(
            controls,
            from_=0,
            to=100,
            number_of_steps=100,
            variable=self.slider_var,
            command=self.on_core_slider,
        )
        self.core_slider.pack(fill=tk.X, pady=6)

        self.core_progress = ctk.CTkProgressBar(controls)
        self.core_progress.pack(fill=tk.X, pady=6)
        self.core_progress.set(self.progress_var.get())

        self.slider_status = ctk.CTkLabel(controls, text=f"Slider Value: {self.slider_var.get():.0f}")
        self.slider_status.pack(anchor="w", pady=(2, 6))

        self.open_dialog_button = ctk.CTkButton(controls, text="Open CTkInputDialog", command=self.show_input_dialog)
        self.open_dialog_button.pack(fill=tk.X, pady=4)

        self.open_toplevel_button = ctk.CTkButton(controls, text="Open CTkToplevel", command=self.open_toplevel_demo)
        self.open_toplevel_button.pack(fill=tk.X, pady=4)

        theme_btn = ctk.CTkButton(controls, text="ThemeManager Snapshot", command=self.show_theme_info)
        theme_btn.pack(fill=tk.X, pady=4)

        self.add_ctk_tooltip(self.core_entry, "CTkEntry accepts text")
        self.add_ctk_tooltip(self.core_textbox, "CTkTextbox supports multiline text")
        self.add_ctk_tooltip(self.core_slider, "CTkSlider drives CTkProgressBar")
        self.add_ctk_tooltip(self.open_dialog_button, "Opens CTkInputDialog")
        self.add_ctk_tooltip(self.open_toplevel_button, "Opens CTkToplevel window")

        self.add_tk_tooltip(self.core_checkbox, "Legacy tkinter-tooltip ToolTip on a CTkCheckBox")
        self.add_tk_tooltip(self.core_radio_a, "tktooltip on radio button A")
        self.add_tk_tooltip(theme_btn, "tktooltip on theme info button")

    def build_dropdowns_lists_tab(self, tab: ctk.CTkFrame) -> None:
        top = ctk.CTkFrame(tab, corner_radius=10)
        top.pack(fill=tk.X, padx=10, pady=(10, 6))

        self.option_menu = ctk.CTkOptionMenu(
            top,
            values=["Blue", "Green", "Orange", "Teal", "Rose"],
            command=lambda choice: self.set_status(f"OptionMenu: {choice}"),
        )
        self.option_menu.pack(side=tk.LEFT, padx=8, pady=8)
        self.option_menu.set("Blue")

        self.combo_box = ctk.CTkComboBox(
            top,
            values=[f"Item {index}" for index in range(1, 21)],
            command=lambda value: self.set_status(f"ComboBox: {value}"),
        )
        self.combo_box.pack(side=tk.LEFT, padx=8, pady=8)

        if CTkScrollableDropdown is not None:
            try:
                self.scrollable_dropdown = CTkScrollableDropdown(
                    attach=self.combo_box,
                    values=[f"Scrollable {i}" for i in range(1, 31)],
                    command=lambda value: self.set_status(f"ScrollableDropdown: {value}"),
                    autocomplete=True,
                    scrollbar=True,
                    height=200,
                    width=250,
                    pagination=False,
                )
            except Exception as exc:
                warn_import("CTkScrollableDropdown runtime", exc)
                ctk.CTkLabel(top, text="[CTkScrollableDropdown failed at runtime]").pack(side=tk.LEFT, padx=8, pady=8)
        else:
            ctk.CTkLabel(top, text="[CTkScrollableDropdown unavailable]").pack(side=tk.LEFT, padx=8, pady=8)

        self.segmented = ctk.CTkSegmentedButton(
            top,
            values=["North", "South", "East", "West"],
            command=lambda value: self.set_status(f"Segmented: {value}"),
        )
        self.segmented.pack(side=tk.LEFT, padx=8, pady=8)
        self.segmented.set("North")

        list_area = ctk.CTkFrame(tab, corner_radius=10)
        list_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        list_header = ctk.CTkLabel(
            list_area,
            text="CTkListbox",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        list_header.pack(anchor="w", padx=12, pady=(10, 2))

        controls = ctk.CTkFrame(list_area)
        controls.pack(fill=tk.X, padx=12, pady=(0, 8))

        self.listbox_status = ctk.CTkLabel(controls, text="Selected: none")
        self.listbox_status.pack(side=tk.LEFT, padx=(4, 8), pady=8)

        ctk.CTkButton(controls, text="Delete Selected", command=self.delete_selected_listbox).pack(
            side=tk.LEFT, padx=4, pady=8
        )
        ctk.CTkButton(controls, text="Activate #3", command=lambda: self.activate_listbox_index(2)).pack(
            side=tk.LEFT, padx=4, pady=8
        )

        if CTkListbox is not None:
            try:
                self.demo_listbox = CTkListbox(
                    list_area,
                    width=320,
                    height=280,
                    command=self.on_listbox_select,
                )
                self.demo_listbox.pack(anchor="w", padx=12, pady=(2, 12))
                for item in [
                    "Alpha",
                    "Bravo",
                    "Charlie",
                    "Delta",
                    "Echo",
                    "Foxtrot",
                    "Golf",
                    "Hotel",
                    "India",
                    "Juliet",
                    "Kilo",
                    "Lima",
                ]:
                    self.demo_listbox.insert("END", item)
            except Exception as exc:
                warn_import("CTkListbox runtime", exc)
                self.demo_listbox = None
        else:
            self.demo_listbox = None
            ctk.CTkLabel(list_area, text="CTkListbox unavailable").pack(anchor="w", padx=12, pady=8)

    def build_containers_tab(self, tab: ctk.CTkFrame) -> None:
        outer = ctk.CTkFrame(tab, corner_radius=10)
        outer.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            outer,
            text="Containers: CTkFrame + CTkScrollableFrame + Separators",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=12, pady=(12, 8))

        row = ctk.CTkFrame(outer)
        row.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        left_frame = ctk.CTkFrame(row)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        scroll_frame = ctk.CTkScrollableFrame(left_frame, width=380, height=420)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for idx in range(1, 31):
            ctk.CTkLabel(scroll_frame, text=f"Scrollable item {idx:02d}").pack(anchor="w", pady=3, padx=6)

        right_frame = ctk.CTkFrame(row)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))

        ctk.CTkLabel(right_frame, text="Separator demos", font=ctk.CTkFont(size=15, weight="bold")).pack(
            anchor="w", padx=10, pady=(10, 6)
        )

        if Separator is not None:
            try:
                separator_host = ctk.CTkFrame(right_frame)
                separator_host.pack(fill=tk.X, padx=10, pady=8)
                ctk.CTkLabel(separator_host, text="Left").pack(side=tk.LEFT, padx=(0, 8))
                Separator(separator_host, length=120, width=4, orientation="vertical").pack(side=tk.LEFT, padx=4)
                ctk.CTkLabel(separator_host, text="Right").pack(side=tk.LEFT, padx=(8, 0))

                Separator(right_frame, length=260, width=4, orientation="horizontal").pack(fill=tk.X, padx=10, pady=10)
            except Exception as exc:
                warn_import("Separator runtime", exc)
        else:
            ctk.CTkLabel(right_frame, text="Separator unavailable").pack(anchor="w", padx=10, pady=8)

        nested = ctk.CTkFrame(right_frame)
        nested.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        ctk.CTkLabel(nested, text="Nested CTkFrame inside container tab").pack(anchor="w", padx=8, pady=8)
        ctk.CTkButton(
            nested, text="Container Button", command=lambda: self.set_status("Container button clicked")
        ).pack(anchor="w", padx=8, pady=4)

    def build_toggles_groups_tab(self, tab: ctk.CTkFrame) -> None:
        panel = ctk.CTkFrame(tab, corner_radius=10)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="CTkToggleButton + CTkToggleGroup", font=ctk.CTkFont(size=18, weight="bold")).pack(
            anchor="w", padx=12, pady=(12, 10)
        )

        self.toggle_state_label = ctk.CTkLabel(panel, text="ToggleButton state: False")
        self.toggle_state_label.pack(anchor="w", padx=12, pady=6)

        if CTkToggleButton is not None:
            try:
                self.toggle_button = CTkToggleButton(panel, text="Toggle Me", command=self.on_toggle_button)
                self.toggle_button.pack(anchor="w", padx=12, pady=6)

                ctk.CTkButton(panel, text="Programmatic Toggle", command=self.toggle_programmatically).pack(
                    anchor="w", padx=12, pady=(2, 8)
                )
            except Exception as exc:
                warn_import("CTkToggleButton runtime", exc)
                self.toggle_button = None
        else:
            self.toggle_button = None
            ctk.CTkLabel(panel, text="CTkToggleButton unavailable").pack(anchor="w", padx=12, pady=8)

        self.toggle_group_label = ctk.CTkLabel(panel, text="ToggleGroup value: none")
        self.toggle_group_label.pack(anchor="w", padx=12, pady=6)

        if CTkToggleGroup is not None and CTkToggleButton is not None:
            try:
                toggle_frame = ctk.CTkFrame(panel)
                toggle_frame.pack(anchor="w", padx=12, pady=8)
                self.toggle_group = CTkToggleGroup()
                toggle_btn_names = ["One", "Two", "Three", "Four", "Five"]
                for name in toggle_btn_names:
                    btn = CTkToggleButton(
                        toggle_frame,
                        text=name,
                        toggle_group=self.toggle_group,
                        command=lambda n=name: self.on_toggle_group(n),
                    )
                    btn.pack(side=tk.LEFT, padx=4, pady=4)
            except Exception as exc:
                warn_import("CTkToggleGroup runtime", exc)
                self.toggle_group = None
        else:
            self.toggle_group = None
            ctk.CTkLabel(panel, text="CTkToggleGroup unavailable").pack(anchor="w", padx=12, pady=6)

    def build_carousel_loader_tab(self, tab: ctk.CTkFrame) -> None:
        top = ctk.CTkFrame(tab, corner_radius=10)
        top.pack(fill=tk.X, padx=10, pady=(10, 6))

        ctk.CTkLabel(
            top,
            text="CTkCarousel + CTkLoader",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=12, pady=(12, 8))

        action_row = ctk.CTkFrame(top)
        action_row.pack(fill=tk.X, padx=12, pady=(0, 12))
        ctk.CTkButton(action_row, text="Start Loader", command=self.start_loader).pack(side=tk.LEFT, padx=6, pady=8)
        ctk.CTkButton(action_row, text="Stop Loader", command=self.stop_loader).pack(side=tk.LEFT, padx=6, pady=8)
        ctk.CTkButton(action_row, text="Toggle Loader", command=self.toggle_loader).pack(side=tk.LEFT, padx=6, pady=8)

        self.loader_state_label = ctk.CTkLabel(action_row, text="Loader: idle")
        self.loader_state_label.pack(side=tk.LEFT, padx=12, pady=8)

        body = ctk.CTkFrame(tab, corner_radius=10)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.carousel_images = []
        for image_name in ("bear.jpg", "bear2.jpg", "bear3.jpg"):
            image_path = DATA_DIR / image_name
            if not image_path.is_file():
                continue
            try:
                src = Image.open(image_path)
                self.carousel_images.append(ctk.CTkImage(light_image=src, dark_image=src, size=(560, 300)))
            except Exception as exc:
                warn_import(f"carousel image {image_name}", exc)

        self.carousel = ctk.CTkLabel(body, text="", width=560, height=300)
        self.carousel.pack(padx=12, pady=(12, 8), anchor="w")

        nav_row = ctk.CTkFrame(body, fg_color="transparent")
        nav_row.pack(anchor="w", padx=12, pady=(0, 12))
        ctk.CTkButton(nav_row, text="◀ Prev", width=90, command=self.carousel_prev).pack(side=tk.LEFT, padx=(0, 6))
        ctk.CTkButton(nav_row, text="Next ▶", width=90, command=self.carousel_next).pack(side=tk.LEFT, padx=(0, 10))
        self.carousel_indicator = ctk.CTkLabel(nav_row, text="0 / 0")
        self.carousel_indicator.pack(side=tk.LEFT)

        self.carousel_index = 0
        self.show_carousel_index(0)
        self.schedule_carousel_auto_advance()

    def show_carousel_index(self, index: int) -> None:
        total = len(self.carousel_images)
        if total == 0:
            self.carousel.configure(text="No carousel images found in ctkdemo_data/", image=None)
            self.carousel_indicator.configure(text="0 / 0")
            return

        self.carousel_index = index % total
        self.carousel.configure(text="", image=self.carousel_images[self.carousel_index])
        self.carousel_indicator.configure(text=f"{self.carousel_index + 1} / {total}")

    def carousel_prev(self) -> None:
        if not self.carousel_images:
            return
        self.show_carousel_index(self.carousel_index - 1)
        self.schedule_carousel_auto_advance()

    def carousel_next(self) -> None:
        if not self.carousel_images:
            return
        self.show_carousel_index(self.carousel_index + 1)
        self.schedule_carousel_auto_advance()

    def schedule_carousel_auto_advance(self) -> None:
        if self.carousel_after_id is not None:
            self.after_cancel(self.carousel_after_id)
            self.carousel_after_id = None
        if len(self.carousel_images) <= 1 or self._closing:
            return
        self.carousel_after_id = self.after(4000, self.carousel_auto_advance)

    def carousel_auto_advance(self) -> None:
        if self._closing or not self.carousel_images:
            return
        self.show_carousel_index(self.carousel_index + 1)
        self.schedule_carousel_auto_advance()

    def build_progress_popup_tab(self, tab: ctk.CTkFrame) -> None:
        panel = ctk.CTkFrame(tab, corner_radius=10)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Progress + Popup widgets", font=ctk.CTkFont(size=18, weight="bold")).pack(
            anchor="w", padx=12, pady=(12, 10)
        )

        btn_row = ctk.CTkFrame(panel)
        btn_row.pack(fill=tk.X, padx=12, pady=6)
        ctk.CTkButton(btn_row, text="Start Progress Popup", command=self.start_progress_popup).pack(
            side=tk.LEFT, padx=6, pady=8
        )
        ctk.CTkButton(btn_row, text="Show CTkInputDialog", command=self.show_input_dialog).pack(
            side=tk.LEFT, padx=6, pady=8
        )
        ctk.CTkButton(btn_row, text="Open CTkToplevel", command=self.open_toplevel_demo).pack(
            side=tk.LEFT, padx=6, pady=8
        )

        ctk.CTkLabel(
            panel,
            text="Right-click anywhere in the app to open ContextMenu from CTkMenuBarPlus.",
            justify="left",
        ).pack(anchor="w", padx=12, pady=10)

        info_box = ctk.CTkTextbox(panel, height=180)
        info_box.pack(fill=tk.BOTH, expand=True, padx=12, pady=(2, 12))
        info_box.insert(
            "1.0",
            "CTkProgressPopup simulation steps:\n"
            "1) Click Start Progress Popup\n"
            "2) Popup appears and progress increments\n"
            "3) Popup closes at 100%\n\n"
            "ContextMenu appears on right-click and provides real actions.\n",
        )

    def build_html_tab(self, tab: ctk.CTkFrame) -> None:
        panel = ctk.CTkFrame(tab, corner_radius=10)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="HtmlFrame (tkinterweb)", font=ctk.CTkFont(size=18, weight="bold")).pack(
            anchor="w", padx=12, pady=(12, 6)
        )

        controls = ctk.CTkFrame(panel)
        controls.pack(fill=tk.X, padx=12, pady=(0, 8))
        ctk.CTkButton(controls, text="Load Sample HTML", command=self.load_sample_html).pack(
            side=tk.LEFT, padx=6, pady=8
        )
        ctk.CTkButton(controls, text="Load python.org", command=self.load_python_org).pack(side=tk.LEFT, padx=6, pady=8)

        host = tk.Frame(panel, bg="#111111")
        host.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        if HtmlFrame is not None:
            try:
                self.html_frame = HtmlFrame(host, messages_enabled=False)
                self.html_frame.pack(fill=tk.BOTH, expand=True)
                self.load_sample_html()
            except Exception as exc:
                warn_import("HtmlFrame runtime", exc)
                self.html_frame = None
                ctk.CTkLabel(panel, text="HtmlFrame failed to initialize").pack(anchor="w", padx=12, pady=8)
        else:
            self.html_frame = None
            ctk.CTkLabel(panel, text="HtmlFrame unavailable").pack(anchor="w", padx=12, pady=8)

    def build_media_player_tab(self, tab: ctk.CTkFrame) -> None:
        panel = ctk.CTkFrame(tab, corner_radius=10)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Media Player (tkinter-videoplayer)", font=ctk.CTkFont(size=18, weight="bold")).pack(
            anchor="w", padx=12, pady=(12, 6)
        )

        ctk.CTkLabel(
            panel,
            text="A bundled demo video is pre-loaded from ctkdemo_data/bear.mp4. Use Load Video to switch files.",
            justify="left",
        ).pack(anchor="w", padx=12, pady=(0, 8))

        controls = ctk.CTkFrame(panel)
        controls.pack(fill=tk.X, padx=12, pady=(0, 8))

        ctk.CTkButton(controls, text="Load Video", command=self.load_video_file).pack(side=tk.LEFT, padx=6, pady=8)
        ctk.CTkButton(controls, text="Play", command=self.video_play).pack(side=tk.LEFT, padx=6, pady=8)
        ctk.CTkButton(controls, text="Pause", command=self.video_pause).pack(side=tk.LEFT, padx=6, pady=8)
        ctk.CTkButton(controls, text="Stop", command=self.video_stop).pack(side=tk.LEFT, padx=6, pady=8)
        ctk.CTkButton(controls, text="Seek +5s", command=lambda: self.video_seek(5)).pack(side=tk.LEFT, padx=6, pady=8)

        self.video_info_label = ctk.CTkLabel(controls, text="No file loaded")
        self.video_info_label.pack(side=tk.LEFT, padx=12, pady=8)

        media_host = tk.Frame(panel, bg="#000000")
        media_host.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        if VideoPlayer is not None:
            try:
                self.video_player = VideoPlayer(media_host, width=640, height=360, controls=True)
                self.video_player.frame.pack(fill=tk.BOTH, expand=True)
            except Exception as exc:
                warn_import("VideoPlayer runtime", exc)
                self.video_player = None
                ctk.CTkLabel(panel, text=f"VideoPlayer failed: {exc}").pack(anchor="w", padx=12, pady=8)
        else:
            self.video_player = None
            ctk.CTkLabel(panel, text="VideoPlayer unavailable (tkinter-videoplayer not installed)").pack(
                anchor="w", padx=12, pady=8
            )

        self.after(200, self.load_default_video)

    def build_layout_helpers_tab(self, tab: ctk.CTkFrame) -> None:
        shell = ctk.CTkFrame(tab, corner_radius=10)
        shell.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            shell, text="Layout Helpers + tkinter-kit + tkinter-page", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=12, pady=(12, 8))

        top_row = ctk.CTkFrame(shell)
        top_row.pack(fill=tk.X, padx=12, pady=6)

        ctk.CTkButton(top_row, text="Open tkinter-kit table", command=self.show_tkk_table_window).pack(
            side=tk.LEFT, padx=6, pady=8
        )

        split = ctk.CTkFrame(shell)
        split.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        left = ctk.CTkFrame(split)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6), pady=6)
        right = ctk.CTkFrame(split)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=6)

        ctk.CTkLabel(left, text="grid_manager + pack_manager demo").pack(anchor="w", padx=8, pady=(8, 4))
        tk_left_host = tk.Frame(left, bg="#252525", height=220)
        tk_left_host.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        self.build_layout_manager_demo(tk_left_host)

        ctk.CTkLabel(right, text="tkinter-kit scrollbar + tkinter-page").pack(anchor="w", padx=8, pady=(8, 4))
        tk_right_host = tk.Frame(right, bg="#252525", height=220)
        tk_right_host.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        self.build_tkk_scroll_and_tkpage_demo(tk_right_host)

    def build_async_tab(self, tab: ctk.CTkFrame) -> None:
        panel = ctk.CTkFrame(tab, corner_radius=10)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            panel, text="async-tkinter-loop + tkinter-async-execute", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=12, pady=(12, 8))

        self.async_label = ctk.CTkLabel(panel, text="Async countdown not started")
        self.async_label.pack(anchor="w", padx=12, pady=6)

        row1 = ctk.CTkFrame(panel)
        row1.pack(fill=tk.X, padx=12, pady=6)

        @async_handler
        async def async_countdown() -> None:
            self.set_status("async_handler countdown started")
            for value in range(5, -1, -1):
                if self._closing:
                    return
                self.async_label.configure(text=f"async_handler countdown: {value}")
                await asyncio.sleep(1)
            if not self._closing:
                self.async_label.configure(text="async_handler done")
                self.set_status("async_handler countdown complete")

        self.async_countdown = async_countdown

        ctk.CTkButton(row1, text="Run @async_handler Countdown", command=self.async_countdown).pack(
            side=tk.LEFT,
            padx=6,
            pady=8,
        )

        row2 = ctk.CTkFrame(panel)
        row2.pack(fill=tk.X, padx=12, pady=6)

        ctk.CTkButton(row2, text="Run tae.execute Coroutine", command=self.run_tae_coroutine).pack(
            side=tk.LEFT,
            padx=6,
            pady=8,
        )
        ctk.CTkButton(row2, text="tae.stop()", command=self.stop_tae_runtime).pack(side=tk.LEFT, padx=6, pady=8)

        self.tae_label = ctk.CTkLabel(panel, text="tae idle")
        self.tae_label.pack(anchor="w", padx=12, pady=(6, 10))

        summary = ctk.CTkTextbox(panel, height=180)
        summary.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        summary.insert(
            "1.0",
            "This tab demonstrates two async models:\n"
            "- async-tkinter-loop: @async_handler + async_mainloop(root)\n"
            "- tkinter-async-execute: tae.start(), tae.execute(coro, root), tae.stop()\n"
            "No threads are used.\n",
        )

    def build_icons_tab(self, tab: ctk.CTkFrame) -> None:
        panel = ctk.CTkFrame(tab, corner_radius=10)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            panel, text="Bootstrap Icons (ttkbootstrap-icons-bs)", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=12, pady=(12, 8))

        if BootstrapIcon is None:
            ctk.CTkLabel(panel, text="BootstrapIcon unavailable (install ttkbootstrap-icons-bs)").pack(
                anchor="w", padx=12, pady=8
            )
            return

        controls = ctk.CTkFrame(panel)
        controls.pack(fill=tk.X, padx=12, pady=6)

        self._icon_size_var = tk.IntVar(value=32)
        ctk.CTkLabel(controls, text="Size:").pack(side=tk.LEFT, padx=(6, 2))
        size_slider = ctk.CTkSlider(controls, from_=16, to=64, number_of_steps=6, variable=self._icon_size_var)
        size_slider.pack(side=tk.LEFT, padx=6)
        self._icon_size_label = ctk.CTkLabel(controls, text="32")
        self._icon_size_label.pack(side=tk.LEFT, padx=(0, 12))

        self._icon_style_var = tk.StringVar(value="outline")
        ctk.CTkLabel(controls, text="Style:").pack(side=tk.LEFT, padx=(6, 2))
        ctk.CTkSegmentedButton(
            controls, values=["outline", "fill"], variable=self._icon_style_var, command=self._refresh_icon_grid
        ).pack(side=tk.LEFT, padx=6)

        ctk.CTkButton(controls, text="Refresh Grid", command=self._refresh_icon_grid, width=100).pack(
            side=tk.RIGHT, padx=6, pady=6
        )

        self._icon_size_var.trace_add("write", lambda *_: self._on_icon_size_change())

        self._icon_grid_frame = ctk.CTkScrollableFrame(panel, corner_radius=8)
        self._icon_grid_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        self._icon_refs: list[Any] = []  # prevent GC of PhotoImages
        self._refresh_icon_grid()

    def _on_icon_size_change(self) -> None:
        self._icon_size_label.configure(text=str(self._icon_size_var.get()))

    def _refresh_icon_grid(self, *_args: Any) -> None:
        for widget in self._icon_grid_frame.winfo_children():
            widget.destroy()
        self._icon_refs.clear()

        icon_names = [
            "house", "star", "heart", "gear", "camera", "play-circle", "search",
            "bell", "bookmark", "calendar", "chat", "cloud", "envelope", "eye",
            "flag", "folder", "lightning", "lock", "pencil", "person",
            "shield", "trash", "trophy", "wifi", "arrow-right", "check-circle",
            "exclamation-triangle", "info-circle", "x-circle", "download",
            "upload", "file-earmark", "clipboard", "clock", "cpu", "diagram-3",
        ]
        size = self._icon_size_var.get()
        style = self._icon_style_var.get()
        cols = max(1, 6)

        for idx, name in enumerate(icon_names):
            row, col = divmod(idx, cols)
            try:
                icon = BootstrapIcon(name, size=size, color="#DCE4EE", style=style)
                frame = ctk.CTkFrame(self._icon_grid_frame, corner_radius=6)
                frame.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
                lbl = tk.Label(frame, image=icon.image, text=name, compound="top", bg="#2b2b2b", fg="#DCE4EE", font=("Helvetica", 9))
                lbl.pack(padx=6, pady=6)
                self._icon_refs.append(icon)
            except Exception:
                placeholder = ctk.CTkLabel(self._icon_grid_frame, text=name, font=ctk.CTkFont(size=10))
                placeholder.grid(row=row, column=col, padx=4, pady=4)

        for c in range(cols):
            self._icon_grid_frame.columnconfigure(c, weight=1)

        self.set_status(f"Loaded {len(icon_names)} icons ({size}px, {style})")

    def build_themed_text_tab(self, tab: ctk.CTkFrame) -> None:
        panel = ctk.CTkFrame(tab, corner_radius=10)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            panel, text="ThemedText + ScrolledText (ttk-text)", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=12, pady=(12, 8))

        if ThemedText is None:
            ctk.CTkLabel(panel, text="ThemedText unavailable (install ttk-text)").pack(anchor="w", padx=12, pady=8)
            return

        split = ctk.CTkFrame(panel)
        split.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        left = ctk.CTkFrame(split)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6), pady=6)
        ctk.CTkLabel(left, text="ThemedText (basic)", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=8, pady=(8, 4)
        )
        tk_host_left = tk.Frame(left, bg="#2b2b2b")
        tk_host_left.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        themed_text = ThemedText(tk_host_left, height=12, width=40)
        themed_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        themed_text.insert("1.0", "ThemedText: a ttk-themed Text widget.\n\n"
                           "It auto-adapts to the current ttk theme\n"
                           "and supports focus/hover/pressed states.\n\n"
                           "Try typing here — standard Text API applies.")

        right = ctk.CTkFrame(split)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=6)
        ctk.CTkLabel(right, text="ScrolledText (with scrollbars)", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=8, pady=(8, 4)
        )
        tk_host_right = tk.Frame(right, bg="#2b2b2b")
        tk_host_right.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        if TtkScrolledText is not None:
            scrolled = TtkScrolledText(tk_host_right, vertical=True, horizontal=True, height=12, width=40)
            scrolled.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
            long_text = "\n".join(
                f"Line {i:03d}: ScrolledText wraps ThemedText with automatic scrollbars."
                for i in range(1, 51)
            )
            scrolled.insert("1.0", long_text)
        else:
            ctk.CTkLabel(tk_host_right, text="ScrolledText unavailable").pack(padx=8, pady=8)

        info = ctk.CTkTextbox(panel, height=80)
        info.pack(fill=tk.X, padx=12, pady=(0, 12))
        info.insert(
            "1.0",
            "ttk-text provides ThemedText (ttk-themed tk.Text) and ScrolledText\n"
            "(ThemedText + automatic scrollbars). Both use standard Text widget API.\n"
            "Styling is done via ttk Style on 'ThemedText.TEntry'.\n",
        )

    def build_devtools_tab(self, tab: ctk.CTkFrame) -> None:
        panel = ctk.CTkFrame(tab, corner_radius=10)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            panel, text="Dev Tools (tklive)", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=12, pady=(12, 8))

        if tklive_live is None:
            ctk.CTkLabel(panel, text="tklive unavailable (install tklive)").pack(anchor="w", padx=12, pady=8)

        info = ctk.CTkTextbox(panel, height=260)
        info.pack(fill=tk.BOTH, expand=True, padx=12, pady=(6, 12))
        info.insert(
            "1.0",
            "tklive — Hot-Reload for Tkinter / CustomTkinter\n"
            "=" * 48 + "\n\n"
            "tklive enables live hot-reloading of this app during development.\n"
            "When enabled, saving any watched .py file auto-reloads the UI.\n\n"
            "Features:\n"
            "  • Watches .py files for changes\n"
            "  • Preserves widget states (entries, sliders, checkboxes, etc.)\n"
            "  • Preserves window position and size\n"
            "  • Manual reload: Ctrl+R\n\n"
            "Supported widgets for state preservation:\n"
            "  tkinter:  Entry, Text, Scale, Spinbox, Listbox, etc.\n"
            "  ttk:      Combobox, Entry, Notebook, Treeview, etc.\n"
            "  ctk:      CTkEntry, CTkTextbox, CTkComboBox, CTkSlider,\n"
            "            CTkCheckBox, CTkSwitch, CTkSegmentedButton, CTkTabview\n\n"
            "Usage in code:\n"
            "  from tklive import live\n"
            "  live(root, __file__)  # before mainloop()\n\n"
            "Status: " + ("ENABLED — hot-reload is active" if tklive_live is not None else "DISABLED — tklive not installed") + "\n",
        )

    def set_appearance(self, mode: str) -> None:
        normalized = mode.strip().lower()
        if normalized == "dark":
            ctk.set_appearance_mode("dark")
            self.set_status("Appearance mode -> Dark")
        elif normalized == "light":
            ctk.set_appearance_mode("light")
            self.set_status("Appearance mode -> Light")
        else:
            ctk.set_appearance_mode("system")
            self.set_status("Appearance mode -> System")

    def show_theme_info(self) -> None:
        preview = str(getattr(ctk.ThemeManager, "theme", {}))[:800]
        top = ctk.CTkToplevel(self)
        top.title("ThemeManager")
        top.geometry("760x420")
        text = ctk.CTkTextbox(top)
        text.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        text.insert("1.0", f"ThemeManager preview:\n\n{preview}\n")
        self.set_status("Opened ThemeManager preview")

    def on_core_slider(self, value: float) -> None:
        v = max(0.0, min(100.0, value))
        self.core_progress.set(v / 100.0)
        self.slider_status.configure(text=f"Slider Value: {v:.0f}")
        self.progress_var.set(v / 100.0)

    def show_input_dialog(self) -> None:
        dialog = ctk.CTkInputDialog(text="Type a value:", title="CTkInputDialog Demo")
        response = dialog.get_input()
        self.set_status(f"CTkInputDialog response: {response!r}")

    def open_toplevel_demo(self) -> None:
        top = ctk.CTkToplevel(self)
        top.title("CTkToplevel Demo")
        top.geometry("480x320")
        ctk.CTkLabel(top, text="This is a CTkToplevel", font=ctk.CTkFont(size=18, weight="bold")).pack(
            padx=12,
            pady=(16, 8),
        )
        ctk.CTkEntry(top, placeholder_text="Type here in top-level window").pack(fill=tk.X, padx=12, pady=6)
        ctk.CTkTextbox(top, height=130).pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
        ctk.CTkButton(top, text="Close", command=top.destroy).pack(padx=12, pady=(4, 12))
        self.set_status("Opened CTkToplevel")

    def on_listbox_select(self, value: Any) -> None:
        self.listbox_status.configure(text=f"Selected: {value}")
        self.set_status(f"Listbox selected: {value}")

    def delete_selected_listbox(self) -> None:
        if self.demo_listbox is None:
            self.set_status("CTkListbox unavailable")
            return
        try:
            selected = self.demo_listbox.curselection()
            if selected is None:
                self.set_status("No listbox selection")
                return
            idx = selected[0] if isinstance(selected, (list, tuple)) else selected
            self.demo_listbox.delete(idx)
            self.set_status(f"Deleted listbox index {idx}")
        except (IndexError, TypeError):
            self.set_status("No listbox selection")
        except Exception as exc:
            warn_import("CTkListbox delete", exc)

    def activate_listbox_index(self, index: int) -> None:
        if self.demo_listbox is None:
            return
        try:
            self.demo_listbox.activate(index)
            value = self.demo_listbox.get()
            self.listbox_status.configure(text=f"Activated: {value}")
        except Exception as exc:
            warn_import("CTkListbox activate", exc)

    def on_toggle_button(self) -> None:
        if self.toggle_button is None:
            return
        try:
            state = bool(self.toggle_button.get())
            self.toggle_state_label.configure(text=f"ToggleButton state: {state}")
            self.set_status(f"ToggleButton changed: {state}")
        except Exception as exc:
            warn_import("CTkToggleButton get", exc)

    def toggle_programmatically(self) -> None:
        if self.toggle_button is None:
            return
        try:
            self.toggle_button.toggle()
            self.on_toggle_button()
        except Exception as exc:
            warn_import("CTkToggleButton.toggle", exc)

    def on_toggle_group(self, value: str) -> None:
        self.toggle_group_label.configure(text=f"ToggleGroup value: {value}")
        self.set_status(f"ToggleGroup selected: {value}")

    def start_loader(self) -> None:
        if self.loader_overlay is not None:
            self.loader_state_label.configure(text="Loader: already running")
            return
        try:
            self.loader_overlay = InlineLoaderOverlay(self)
            self.loader_state_label.configure(text="Loader: running")
            self.set_status("Loader started")
        except Exception as exc:
            warn_import("inline loader runtime", exc)

    def stop_loader(self) -> None:
        if self.loader_overlay is None:
            self.loader_state_label.configure(text="Loader: idle")
            return
        try:
            self.loader_overlay.stop_loader()
        except Exception as exc:
            warn_import("CTkLoader.stop_loader", exc)
        self.loader_overlay = None
        self.loader_state_label.configure(text="Loader: stopped")
        self.set_status("Loader stopped")

    def toggle_loader(self) -> None:
        if self.loader_overlay is None:
            self.start_loader()
        else:
            self.stop_loader()

    def start_progress_popup(self) -> None:
        try:
            if self.progress_popup is not None:
                self.progress_popup.close_progress_popup()
        except Exception:
            pass
        try:
            self.progress_popup = InlineProgressPopup(
                self,
                title="Task",
                label="Export",
                message="Preparing...",
                side="right_bottom",
            )
            self.progress_value = 0.0
            self.set_status("Progress popup started")
            self.after(140, self.step_progress_popup)
        except Exception as exc:
            warn_import("CTkProgressPopup runtime", exc)
            self.progress_popup = None

    def step_progress_popup(self) -> None:
        if self.progress_popup is None or self._closing:
            return
        self.progress_value += 0.08
        if self.progress_value >= 1.0:
            try:
                self.progress_popup.update_progress(1.0)
                self.progress_popup.update_message("Done")
                self.progress_popup.close_progress_popup()
            except Exception as exc:
                warn_import("CTkProgressPopup close", exc)
            self.progress_popup = None
            self.set_status("Progress popup complete")
            return

        percent = int(self.progress_value * 100)
        try:
            self.progress_popup.update_progress(self.progress_value)
            self.progress_popup.update_message(f"Working... {percent}%")
        except Exception as exc:
            warn_import("CTkProgressPopup update", exc)
            self.progress_popup = None
            return
        self.after(140, self.step_progress_popup)

    def load_sample_html(self) -> None:
        if self.html_frame is None:
            self.set_status("HtmlFrame unavailable")
            return
        html = """
        <html>
          <head>
            <title>CustomTkinter HTML Demo</title>
          </head>
          <body>
            <h1>HTML Viewer Demo</h1>
            <p>This HTML is loaded via <code>HtmlFrame.load_html()</code>.</p>
            <ul>
              <li>Styled heading</li>
              <li>Paragraph and list</li>
              <li>Inline code and links</li>
            </ul>
            <p><a href="https://www.python.org">Python.org</a></p>
          </body>
        </html>
        """
        try:
            self.html_frame.load_html(html)
            self.html_frame.add_css(
                "body{font-family:Segoe UI,Arial;padding:20px;background:#1b1d24;color:#e9edf5;}"
                "a{color:#7fb4ff;}"
                "code{background:#2c3040;padding:2px 6px;border-radius:4px;}"
            )
            self.set_status("Loaded sample HTML")
        except Exception as exc:
            warn_import("HtmlFrame.load_html", exc)

    def load_python_org(self) -> None:
        if self.html_frame is None:
            return
        try:
            self.html_frame.load_website("https://www.python.org")
            self.set_status("Loaded python.org in HtmlFrame")
        except Exception as exc:
            warn_import("HtmlFrame.load_website", exc)

    def load_video_file(self) -> None:
        if self.video_player is None:
            self.set_status("No video player available")
            return
        path_text = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[
                ("Video Files", "*.mp4 *.mkv *.mov *.avi *.webm"),
                ("All Files", "*.*"),
            ],
        )
        if not path_text:
            self.set_status("No video file selected")
            return
        path = Path(path_text)
        try:
            self.video_player.src = str(path)
            self.video_info_label.configure(text=f"Loaded: {path.name}")
            self.set_status(f"Video loaded: {path.name}")
        except Exception as exc:
            warn_import("VideoPlayer.src", exc)
            self.set_status("Failed to load video")

    def load_default_video(self) -> None:
        default_video = DATA_DIR / "bear.mp4"
        if not default_video.is_file():
            self.video_info_label.configure(text="Demo video missing")
            self.set_status("Demo video not found in ctkdemo_data")
            return

        if self.video_player is None:
            self.video_info_label.configure(text="VideoPlayer unavailable")
            self.set_status("No video player available")
            return

        try:
            self.video_player.src = str(default_video)
            self.video_info_label.configure(text=f"Loaded demo: {default_video.name}")
            self.set_status(f"Demo video loaded: {default_video.name}")
        except Exception as exc:
            warn_import("VideoPlayer.src demo", exc)
            self.video_info_label.configure(text="Demo video failed to load")
            self.set_status("Failed to load demo video")

    def video_play(self) -> None:
        if self.video_player is not None:
            try:
                self.video_player.play()
            except Exception as exc:
                warn_import("VideoPlayer.play", exc)
        self.set_status("Video play")

    def video_pause(self) -> None:
        if self.video_player is not None:
            try:
                self.video_player.pause()
            except Exception as exc:
                warn_import("VideoPlayer.pause", exc)
        self.set_status("Video pause")

    def video_stop(self) -> None:
        if self.video_player is not None:
            try:
                self.video_player.stop()
            except Exception as exc:
                warn_import("VideoPlayer.stop", exc)
        self.set_status("Video stop")

    def video_seek(self, seconds: int) -> None:
        if self.video_player is not None:
            try:
                self.video_player.currentTime = seconds
            except Exception as exc:
                warn_import("VideoPlayer.seek", exc)
        self.set_status(f"Video seek -> {seconds}s")

    def build_layout_manager_demo(self, master: tk.Widget) -> None:
        holder = tk.Frame(master, bg="#1f222d")
        holder.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        grid_host = tk.Frame(holder, bg="#1f222d")
        grid_host.pack(fill=tk.X, padx=0, pady=0)

        try:
            if grid_manager is not None:
                with grid_manager(grid_host) as grid:
                    grid_host.columnconfigure(0, weight=1)
                    grid_host.columnconfigure(1, weight=1)
                    tk.Label(grid_host, text="grid_manager", fg="#dce8ff", bg="#1f222d").grid(
                        row=0,
                        column=0,
                        sticky="w",
                        padx=8,
                        pady=6,
                    )
                    tk.Entry(grid_host).grid(row=0, column=1, sticky="ew", padx=8, pady=6)
                    tk.Label(grid_host, text="Second row", fg="#dce8ff", bg="#1f222d").grid(
                        row=1,
                        column=0,
                        sticky="w",
                        padx=8,
                        pady=6,
                    )
                    tk.Entry(grid_host).grid(row=1, column=1, sticky="ew", padx=8, pady=6)
            else:
                raise RuntimeError("grid_manager unavailable")
        except Exception as exc:
            warn_import("grid_manager runtime", exc)
            tk.Label(grid_host, text="grid_manager unavailable", fg="#ffb3b3", bg="#1f222d").pack(
                anchor="w",
                padx=8,
                pady=8,
            )

        pack_host = tk.Frame(holder, bg="#262a39")
        pack_host.pack(fill=tk.X, padx=8, pady=(10, 6))
        try:
            if pack_manager is not None:
                with pack_manager(pack_host):
                    tk.Label(pack_host, text="pack_manager context", fg="#cde9c8", bg="#262a39").pack(
                        side=tk.LEFT,
                        padx=6,
                        pady=6,
                    )
                    tk.Button(pack_host, text="Action").pack(side=tk.LEFT, padx=6, pady=6)
            else:
                raise RuntimeError("pack_manager unavailable")
        except Exception as exc:
            warn_import("pack_manager runtime", exc)
            tk.Label(pack_host, text="pack_manager unavailable", fg="#ffb3b3", bg="#262a39").pack(
                side=tk.LEFT,
                padx=6,
                pady=6,
            )

    def build_tkk_scroll_and_tkpage_demo(self, master: tk.Widget) -> None:
        top = tk.Frame(master, bg="#1f222d")
        top.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))

        canvas = tk.Canvas(top, bg="#11131a", height=120, highlightthickness=0)
        content = tk.Frame(canvas, bg="#11131a")
        canvas.pack(fill=tk.BOTH, expand=True)

        if tkk is not None:
            try:
                tkk.frame_vertical_scrollbar(top, canvas, content)
                for idx in range(1, 18):
                    tk.Label(
                        content,
                        text=f"tkk scroll item {idx}",
                        fg="#dce8ff",
                        bg="#11131a",
                    ).pack(anchor="w", padx=10, pady=2)
            except Exception as exc:
                warn_import("tkk.frame_vertical_scrollbar", exc)
                tk.Label(top, text="tkinter-kit scrollbar demo failed", fg="#ffb3b3", bg="#1f222d").pack(
                    anchor="w",
                    padx=8,
                    pady=6,
                )
        else:
            tk.Label(top, text="tkinter-kit unavailable", fg="#ffb3b3", bg="#1f222d").pack(anchor="w", padx=8, pady=6)

        bottom = tk.Frame(master, bg="#272c3b")
        bottom.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 8))

        if tkp is not None:
            try:
                desktop = tkp.DesktopFrame(bottom)
                desktop.pack()
                # DesktopFrame exposes sub-frames: bar_frame, files_frame, details_frame,
                # attributes_frame, logs_frame. Populate them directly.
                tk.Label(desktop.bar_frame, text="Quick Access Bar", fg="white", bg="#272c3b").pack(
                    padx=8,
                    pady=6,
                )
                for item in ("Documents", "Images", "Music", "Videos", "Downloads"):
                    tk.Label(desktop.files_frame, text=f"  {item}", fg="#c8d6e5", bg="#1c243a", anchor="w").pack(
                        fill=tk.X,
                        padx=4,
                        pady=1,
                    )
                tk.Label(desktop.details_frame, text="tkinter-page DesktopFrame Demo", fg="#e8ffe9", bg="#182e1d").pack(
                    padx=10,
                    pady=8,
                )
                tk.Label(desktop.details_frame, text="Details panel content here", fg="#a0c8a0", bg="#182e1d").pack(
                    padx=10,
                    pady=4,
                )
                tk.Label(
                    desktop.attributes_frame, text="Attributes: size, date, type", fg="#c8c8e5", bg="#22264a"
                ).pack(
                    padx=8,
                    pady=6,
                )
                tk.Label(desktop.logs_frame, text="Log: DesktopFrame loaded OK", fg="#a0a0a0", bg="#1a1a2e").pack(
                    padx=8,
                    pady=6,
                )
            except Exception as exc:
                warn_import("tkinter-page runtime", exc)
                tk.Label(bottom, text="tkinter-page demo failed", fg="#ffb3b3", bg="#272c3b").pack(
                    anchor="w",
                    padx=8,
                    pady=6,
                )
        else:
            tk.Label(bottom, text="tkinter-page unavailable", fg="#ffb3b3", bg="#272c3b").pack(
                anchor="w", padx=8, pady=6
            )

    def show_tkk_table_window(self) -> None:
        if tkk is None:
            self.set_status("tkinter-kit unavailable")
            return
        headings = ["Name", "Type", "Status"]
        data = [
            ["CTk", "Core", "Ready"],
            ["CTkToggleButton", "Third-party", "Ready"],
            ["HtmlFrame", "Media", "Ready"],
            ["Async Loop", "Async", "Ready"],
        ]
        try:
            tkk.print_table_windows(self, headings, data)
            self.set_status("Opened tkinter-kit table window")
        except Exception as exc:
            warn_import("tkk.print_table_windows", exc)

    def run_tae_coroutine(self) -> None:
        if tae is None:
            self.tae_label.configure(text="tae unavailable")
            self.set_status("tkinter_async_execute unavailable")
            return

        if not self.tae_running:
            try:
                tae.start()
                self.tae_running = True
            except Exception as exc:
                warn_import("tae.start", exc)
                self.tae_label.configure(text="tae start failed")
                return

        async def worker() -> None:
            if self._closing:
                return
            self.tae_label.configure(text="tae worker: begin")
            for idx in range(1, 6):
                await asyncio.sleep(0.7)
                if self._closing:
                    return
                self.tae_label.configure(text=f"tae worker step {idx}/5")
            if not self._closing:
                self.tae_label.configure(text="tae worker done")
                self.set_status("tae.async_execute coroutine complete")

        try:
            tae.async_execute(worker(), wait=False, visible=False, pop_up=False)
            self.set_status("tae.async_execute coroutine started")
        except Exception as exc:
            warn_import("tae.async_execute", exc)

    def stop_tae_runtime(self) -> None:
        if tae is None or not self.tae_running:
            self.tae_label.configure(text="tae already stopped")
            return
        try:
            tae.stop()
            self.tae_running = False
            self.tae_label.configure(text="tae stopped")
            self.set_status("tae.stop() complete")
        except Exception as exc:
            warn_import("tae.stop", exc)

    def on_close(self) -> None:
        self._closing = True

        try:
            if self.loader_overlay is not None:
                self.loader_overlay.stop_loader()
        except Exception:
            pass

        try:
            if self.progress_popup is not None:
                self.progress_popup.close_progress_popup()
        except Exception:
            pass

        if tae is not None and self.tae_running:
            try:
                tae.stop()
            except Exception:
                pass

        self.destroy()


def main() -> None:
    app = CtkMegaDemo()
    if tklive_live is not None:
        tklive_live(app, __file__)
    if async_mainloop is not None:
        async_mainloop(app)
    else:
        app.mainloop()


if __name__ == "__main__":
    main()
