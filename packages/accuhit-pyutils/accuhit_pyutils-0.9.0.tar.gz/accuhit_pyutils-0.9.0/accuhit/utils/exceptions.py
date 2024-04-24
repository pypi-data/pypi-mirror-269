# -*- coding: utf-8 -*-


class CommonRuntimeException(Exception):
    @property
    def code(self):
        return self.args[0]

    @property
    def params(self):
        return self.args[1:] if len(self.args) > 1 else ()
