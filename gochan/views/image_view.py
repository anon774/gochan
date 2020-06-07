from typing import Optional

from asciimatics.effects import Print
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.renderers import ColourImageFile
from asciimatics.screen import Screen
from asciimatics.widgets import Frame

from gochan.models import AppContext
from gochan.view_models import ImageVM


class ImageView(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=False
                         )

        self.set_theme("user_theme")

        self._data_context: Optional[ImageVM] = None

        self._image_effect = None

    def bind(self, context: ImageVM):
        if self._data_context is not None:
            self._data_context.on_property_changed.remove(self._context_changed)

        self._data_context = context
        self._data_context.on_property_changed.add(self._context_changed)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord("q"):
                if self._image_effect is not None:
                    self._scene.remove_effect(self._image_effect)
                    self._image_effect = None

                raise NextScene("Thread")

        return super().process_event(event)

    def _context_changed(self, property_name: str):
        if property_name == "image":
            if self._data_context is not None and self._data_context.image is not None:
                self._image_effect = Print(self.screen, ColourImageFile(
                    self._screen, self._data_context.image, height=self._screen.height), -1)
                self._scene.add_effect(self._image_effect)
