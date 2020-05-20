import sys

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import THEMES, Button, Divider, Frame, Layout, ListBox, Text, TextBox, Widget

from gochan.config import BROWSER_PATH, THEME
from gochan.controller import Controller
from gochan.data import Bbsmenu, BoardHeader, ThreadHeader
from gochan.key import KeyLogger
from gochan.views import BbsmenuView, BoardView, ResponseForm, ThreadView, ImageView


def demo(screen: Screen, scene: Scene):
    bbsmenu_view = BbsmenuView(screen)
    board_view = BoardView(screen)
    thread_view = ThreadView(screen)
    resform = ResponseForm(screen)
    image_view = ImageView(screen)
    keylog = KeyLogger(screen)

    Controller.register_views((bbsmenu_view, "Bbsmenu"), (board_view, "Board"), (thread_view, "Thread"),
                              (resform, "ResponseForm"), (image_view, "ImageView"))
    Controller.bbsmenu.update_data()

    scenes = [
        # Scene([keylog], -1, name="Keylog"),
        Scene([bbsmenu_view], -1, name="Bbsmenu"),
        Scene([board_view], -1, name="Board"),
        Scene([thread_view], -1, name="Thread"),
        Scene([resform], -1, name="ResponseForm"),
        Scene([image_view], -1, name="ImageView")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


def main():
    # Enable user theme
    THEMES["user_theme"] = THEME

    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == "__main__":
    main()
