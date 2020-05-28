from typing import Callable

from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Widget

from gochan.config import KEY_BINDINGS
from gochan.controller import controller
from gochan.models import Bbsmenu, BoardHeader
from gochan.widgets import ListBoxK


class BbsmenuView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         on_load=self._on_load_,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False,
                         title="Bbs Menu",
                         )

        self.set_theme("user_theme")

        self._model = None

        self._keybindings = KEY_BINDINGS["bbsmenu"]

        self._cat_list = ListBoxK(
            Widget.FILL_COLUMN,
            [],
            self._keybindings,
            name="cat_list",
            add_scroll_bar=True,
            on_change=self._on_pick_c,
            on_select=self._on_select_c,
        )

        self._board_list = ListBoxK(
            Widget.FILL_COLUMN,
            [],
            self._keybindings,
            name="board_list",
            add_scroll_bar=True,
            on_change=self._on_pick_b,
            on_select=self._on_select_b,
        )

        layout = Layout([30, 70], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._cat_list, 0)
        layout.add_widget(self._board_list, 1)

        self.fix()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: Bbsmenu):
        self._model = model

        if self._model is not None:
            self._cat_list.options = self._model.get_items()
        else:
            self._cat_list.options = []

    def _on_load_(self, new_value=None):
        self._cat_list.value = new_value
        self._on_pick_c()

    def _on_pick_c(self):
        self.save()

        if "cat_list" in self.data:
            index = self.data['cat_list']
            if index is not None:
                self._board_list.options = self._model.categories[index].get_items()

    def _on_select_c(self):
        self.save()
        index = self.data['cat_list']
        self._board_list.options = self._model.categories[index].get_items()
        self.switch_focus(self._layouts[0], 1, 0)

    def _on_pick_b(self):
        pass

    def _on_select_b(self):
        self.save()
        index1 = self.data['cat_list']
        index2 = self.data['board_list']
        board_hdr = self._model.categories[index1].boards[index2]
        controller.board.set_data(board_hdr)
        raise NextScene(controller.board.scene_name)
