# -*- coding: utf-8 -*-
from apistar.client.transports import HTTPTransport


class ArkindexHTTPTransport(HTTPTransport):
    def __init__(self, verify=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verify = verify

    def get_request_options(self, *args, **kwargs):
        options = super().get_request_options(*args, **kwargs)
        options["timeout"] = (30, 60)
        options["verify"] = self.verify
        return options
