import re
import tempfile
import urllib
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Tuple, TypeVar

from asciimatics.exceptions import NextScene

from gochan.browser import download_image
from gochan.client import client
from gochan.config import USE_CACHE
from gochan.data import BoardHeader, Thread, ThreadHeader
from gochan.storage import storage

if TYPE_CHECKING:
    from gochan.views import BbsmenuView, BoardView, ThreadView, ResponseForm, ImageView


T = TypeVar('T')


class ViewController(Generic[T]):
    def __init__(self, view, name):
        super().__init__()
        self._view: T = view
        self.scene_name: str = name


class BbsmenuViewController(ViewController["BbsmenuView"]):
    def update_data(self):
        m = client.get_bbsmenu()
        self._view.model = m


class BoardViewController(ViewController["BoardView"]):
    def set_data(self, hdr: BoardHeader):
        m = client.get_board(hdr.server, hdr.board)
        self._view.model = m

    def update_data(self):
        old = self._view.model

        if old is not None:
            m = client.get_board(old.server, old.board)
            self._view.model = m


class ThreadViewController(ViewController["ThreadView"]):
    def set_data(self, hdr: ThreadHeader):
        m = client.get_thread(hdr.server, hdr.board, hdr.key)
        self._view.model = m

    def update_data(self):
        old = self._view.model

        if old is not None:
            m = client.get_thread(old.server, old.board, old.key)
            self._view.model = m


class ResponseFormController(ViewController["ResponseForm"]):
    def set_target(self, target: Thread):
        self._view.target = target


class ImageViewController(ViewController["ImageView"]):
    def set_image(self, url: str):
        if USE_CACHE:
            file_name = re.sub(r'https?://|/', "", url)

            cache = storage.get_cache(file_name)
            if cache is not None:
                self._view.image = cache
            else:
                data = download_image(url)
                path = storage.store_cache(file_name, data)
                self._view.image = path
        else:
            data = download_image(url)
            f = tempfile.NamedTemporaryFile()
            f.write(data)
            self._view.image = f.name
            f.close()


class Controller:
    def __init__(self):
        super().__init__()
        self.bbsmenu: BbsmenuViewController = None
        self.board: BoardViewController = None
        self.thread: ThreadViewController = None
        self.resform: ResponseFormController = None
        self.image: ImageViewController = None

    def register_views(self, bbsmenu: Tuple["BoardView", str], board: Tuple["BoardView", str],
                       thread: Tuple["ThreadView", str], resform: Tuple["ResponseForm", str],
                       image: Tuple["ImageView", str]):
        self.bbsmenu = BbsmenuViewController(bbsmenu[0], bbsmenu[1])
        self.board = BoardViewController(board[0], board[1])
        self.thread = ThreadViewController(thread[0], thread[1])
        self.resform = ResponseFormController(resform[0], resform[1])
        self.image = ImageViewController(image[0], image[1])


controller = Controller()
