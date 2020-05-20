from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Tuple, TypeVar

from asciimatics.exceptions import NextScene

from gochan.client import client
from gochan.data import BoardHeader, Thread, ThreadHeader

if TYPE_CHECKING:
    from gochan.views import BbsmenuView, BoardView, ThreadView, ResponseForm, ImageView


T = TypeVar('T')


class ViewController():
    def __init__(self, view, name):
        super().__init__()
        self._view = view
        self._scene_name = name

    def show(self):
        raise NextScene(self._scene_name)


class BbsmenuViewController(ViewController):
    def update_data(self):
        m = client.get_bbsmenu()
        self._view.model = m


class BoardViewController(ViewController):
    def set_data(self, hdr: BoardHeader):
        m = client.get_board(hdr.server, hdr.board)
        self._view.model = m

    def update_data(self):
        old = self._view.model

        if old is not None:
            m = client.get_board(old.server, old.board)
            self._view.model = m


class ThreadViewController(ViewController):
    def set_data(self, hdr: ThreadHeader):
        m = client.get_thread(hdr.server, hdr.board, hdr.key)
        self._view.model = m

    def update_data(self):
        old = self._view.model

        if old is not None:
            m = client.get_thread(old.server, old.board, old.key)
            self._view.model = m


class ResponseFormController(ViewController):
    def set_target(self, target: Thread):
        self._view.target = target


class ImageViewController(ViewController):
    def set_image(self, file_name: str):
        self._view.image = file_name


class Controller:
    bbsmenu: BbsmenuViewController = None
    board: BoardViewController = None
    thread: ThreadViewController = None
    resform: ResponseFormController = None

    @classmethod
    def register_views(cls, bbsmenu: Tuple["BoardView", str], board: Tuple["BoardView", str],
                       thread: Tuple["ThreadView", str], resform: Tuple["ResponseForm", str],
                       image: Tuple["ImageView", str]):
        cls.bbsmenu = BbsmenuViewController(bbsmenu[0], bbsmenu[1])
        cls.board = BoardViewController(board[0], board[1])
        cls.thread = ThreadViewController(thread[0], thread[1])
        cls.resform = ResponseFormController(resform[0], resform[1])
        cls.image = ImageViewController(image[0], image[1])
