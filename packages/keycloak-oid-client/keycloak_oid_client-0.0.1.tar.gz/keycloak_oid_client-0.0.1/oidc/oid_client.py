from abc import ABC, abstractmethod


class OIDClient(ABC):
    @abstractmethod
    def get_access_token(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def logout(self):
        pass
