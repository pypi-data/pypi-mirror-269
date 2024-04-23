from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frontengine.ui.main_ui import FrontEngineMainUI
from PySide6.QtGui import QAction

from frontengine.utils.multi_language.language_wrapper import language_wrapper


def build_how_to_menu(ui_we_want_to_set: FrontEngineMainUI) -> None:
    ui_we_want_to_set.menu_bar.how_to_menu = ui_we_want_to_set.menu_bar.addMenu(
        language_wrapper.language_word_dict.get("menu_bar_language")
    )
