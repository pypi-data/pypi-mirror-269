"""A module to set up the connections to a Tableau server"""
from typing import Optional
import tableauserverclient as TSC
from loguru import logger


class ServerConnector:
    """
    This class provides a connector to a server using Tableau Server Client (TSC) library.

    Args:
        site_name (str): The name of the site on the server.
        server_url (str): The URL of the server.
        token_name (str): The name of the personal access token.
        token_secret (str): The secret of the personal access token.

    Attributes:
        server_name (Optional[str]): The name of the server.
        server_url (str): The URL of the server.
        token_name (str): The name of the personal access token.
        token_secret (str): The secret of the personal access token.
        authentication (Optional[TSC.PersonalAccessTokenAuth]): The authentication object.
        server (Optional[TSC.Server]): The server object.

    Methods:
        connect(): Connects to the server using the provided credentials.

    Properties:
        server (Optional[TSC.Server]): The server object property.
        authentication (Optional[TSC.PersonalAccessTokenAuth]): The authentication object property.
    """

    def __init__(self, site_name, server_url, token_name, token_secret):
        """

        :param site_name:
        :param server_url:
        :param token_name:
        :param token_secret:
        """
        self.server_name: Optional[str] = site_name.strip()
        self.server_url: str = server_url.strip()
        self.token_name: str = token_name.strip()
        self.token_secret: str = token_secret.strip()
        self.authentication: Optional[TSC.PersonalAccessTokenAuth] = None
        self.server: Optional[TSC.Server] = None

    def __repr__(self):
        """

        :return:
        """
        return "<Server {server_name} server_object={_server} auth_object={_authentication}>".format(
            **self.__dict__
        )

    @property
    def server(self) -> Optional[TSC.Server]:
        """

        :return:
        """
        return self._server

    @server.setter
    def server(self, value):
        """

        :param value:
        """
        if value is None:
            self._server = TSC.Server(self.server_url, use_server_version=True)
        elif not isinstance(value, TSC.Server):
            raise TypeError("server must be of TSC.Server class")
        else:
            self._server = value

    @property
    def authentication(self) -> Optional[TSC.PersonalAccessTokenAuth]:
        """

        :return:
        """
        return self._authentication

    @authentication.setter
    def authentication(self, value):
        """

        :param value:
        """
        if value is None:
            self._authentication = TSC.PersonalAccessTokenAuth(
                self.token_name,
                self.token_secret,
                self.server_name,
            )
        elif not isinstance(value, TSC.PersonalAccessTokenAuth):
            raise TypeError(
                "authentication must be of  TSC.PersonalAccessTokenAuth class"
            )
        else:
            self._authentication = value

    def connect(self):
        """

        :return:
        """
        connection = self.server.auth.sign_in(self.authentication)
        return connection
