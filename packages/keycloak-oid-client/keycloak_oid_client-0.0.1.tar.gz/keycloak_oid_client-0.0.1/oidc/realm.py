from abc import ABC


class Realm(ABC):
    def __init__(self, server_url: str, name: str):
        self.server_url = server_url
        self.name = name
