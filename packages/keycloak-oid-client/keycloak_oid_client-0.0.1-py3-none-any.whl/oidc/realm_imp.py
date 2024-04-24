from keycloak.realm import KeycloakRealm

from oidc.oid_client import OIDClient
from oidc.oid_client_imp import OIDClientImp
from oidc.realm import Realm


class RealmImp(Realm):
    def __init__(self, auth_server: str, name: str):
        super().__init__(auth_server, name)
        self.realm = KeycloakRealm(server_url=auth_server, realm_name=name)

    def create_client(self, client_id: str, client_key: str) -> OIDClient:
        return OIDClientImp(self.realm.open_id_connect(client_id, client_key))
