from keycloak.openid_connect import KeycloakOpenidConnect

from oidc.oid_client import OIDClient


class OIDClientImp(OIDClient):
    def __init__(self, oid_client: KeycloakOpenidConnect):
        self.oid_client = oid_client
        self.refresh_token = None

    def get_access_token(self, username: str, password: str) -> str:
        response = self.oid_client.password_credentials(username, password)
        self.refresh_token = response['refresh_token']
        return response['access_token']

    def logout(self):
        if self.refresh_token:
            self.oid_client.logout(self.refresh_token)
