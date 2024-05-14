import logging
import os
from typing import List

from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config
from starlette.requests import Request

from backend.database_models.user import User
from backend.services.auth.base import BaseOAuthStrategy


class GoogleOAuthStrategy(BaseOAuthStrategy):
    """
    Google OAuth2.0 strategy.
    """

    NAME = "Google OAuth"
    OAUTH_NAME = "google"
    GOOGLE_DISCOVERY_DOCUMENT_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    GOOGLE_DEFAULT_SCOPE = "openid email profile"

    def __init__(self):
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

        if any([client_id is None, client_secret is None]):
            raise ValueError(
                "To use Google OAuth, please set the GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
            )

        try:
            config = Config(".env")
            self.oauth = OAuth(config)
            self.oauth.register(
                name=self.DEFAULT_OAUTH_NAME,
                server_metadata_url=self.GOOGLE_DISCOVERY_DOCUMENT_URL,
                client_kwargs={"scope": self.GOOGLE_DEFAULT_SCOPE},
            )
        except Exception as e:
            logging.ERROR(f"Error during initializing of GoogleOAuthStrategy: {str(e)}")
            raise

    @staticmethod
    def get_required_payload() -> List[str]:
        """
        Retrieves the required /login payload for the Auth strategy.

        Returns:
            List[str]: List of required variables.
        """
        return []

    async def login(self, request: Request) -> dict | None:
        """
        Redirects to the /auth endpoint for user to sign onto their Google account.

        Args:
            request (Request): Current request.

        Returns:
            dict | None: Returns the user as dict to set the app session, or None.
        """
        redirect_uri = request.url_for("auth")
        return await self.oauth.google.authorize_redirect(request, redirect_uri)

    async def authenticate(self, request: Request) -> dict | None:
        """
        Authenticates the current user using their Google account.

        Args:
            request (Request): Current request.

        Returns:
            dict | None: Returns the user as dict to set the app session, or None.
        """
        return await self.oauth.google.authorized_access_token(request)
