import re

from typing import List

from gochan.models import Thread, Response

link_reg = re.compile(r'(https?://.*?)(?=$|\n| )')


class ResponseVM:
    def __init__(self, model: Response, link_idx: int):
        super().__init__()

        self._model = model
        self.links = []

        def replace_link(match):
            nonlocal link_idx

            url = match.group(1)
            self.links.append(url)
            repl = url + "(" + str(link_idx) + ")"
            link_idx += 1
            return repl

        self.message = link_reg.sub(replace_link, model.message)

    @property
    def number(self):
        return self._model.number

    @property
    def name(self):
        return self._model.name

    @property
    def mail(self):
        return self._model.mail

    @property
    def date(self):
        return self._model.date

    @property
    def id(self):
        return self._model.id


class ThreadVM:
    def __init__(self, model: Thread):
        super().__init__()

        self._model = model
        self.responses: List[ResponseVM] = []
        self.links: str = []

        for r in self._model.responses:
            vm = ResponseVM(r, len(self.links))

            self.responses.append(vm)
            self.links.extend(vm.links)

    @property
    def server(self):
        return self._model.server

    @property
    def board(self):
        return self._model.board

    @property
    def key(self):
        return self._model.key

    @property
    def title(self):
        return self._model.title

    @property
    def is_pastlog(self):
        return self._model.is_pastlog

    def add_responses(self, responses: List[Response]):
        self._model.add_responses(responses)

        for r in responses:
            vm = ResponseVM(r, len(self.links))

            self.responses.append(vm)
            self.links.extend(vm.links)
