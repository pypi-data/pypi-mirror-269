import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from msal import (
    ConfidentialClientApplication,
    Prompt,
    PublicClientApplication,
    TokenCache,
)
from msal_extensions import PersistedTokenCache, build_encrypted_persistence


class IAuthenticator(ABC):
    """
    Interface class for authenticator.
    """

    @abstractmethod
    def authenticate(self) -> Optional[dict[str, Any]]:
        """
        Performs the authentication process and returns the authentication results.

        Returns:
            Optional[Dict[str, Any]]: The authentication results, typically including the
            access token, expiration time, etc.
        """
        pass

    @abstractmethod
    def renew_token(self, refresh_token: str) -> Optional[dict[str, Any]]:
        """
        Renews the access token using the provided refresh token.

        Args:
            refresh_token (str): The refresh token for token renewal.

        Returns:
            Optional[Dict[str, Any]]: The renewed authentication results, typically including
            the new access token, expiration time, etc.
        """
        pass


@dataclass
class MSALInteractiveAuthenticator(IAuthenticator):
    """
    This class serves as an interactive authenticator for managing authentication tokens in
    scenarios where user interaction is required. It utilizes the Microsoft Authentication Library
    (MSAL) and enables interactive token acquisition, such as via a local browser.

    Attributes:
        authorization_endpoint (str): The authorization endpoint URL of the Azure AD B2C tenant.
        tenant (str): The Azure AD B2C tenant.
        policy (str): The policy associated with the authentication flow.
        app_client_id (str): The client ID of the application.
        api_client_id (str): The client ID for the API. This is used to authenticate with the API.
        cache (Optional[TokenCache]): An optional cache for tokens. If provided, the Authenticator
            will use this cache to store and retrieve tokens, reducing the need for repeated
            authentications.
    """

    authorization_endpoint: str
    tenant: str
    policy: str
    app_client_id: str
    api_client_id: str
    cache: Optional[TokenCache] = None

    def authenticate(self) -> Optional[dict[str, Any]]:
        """
        Performs the authentication process and returns the authentication results.

        Returns:
            Optional[Dict[str, Any]]: The authentication results, typically including the
            access token, expiration time, etc.
        """

        # Please visit the link https://pypi.org/project/msal/ for implementation details

        authority = f"{self.authorization_endpoint}/{self.tenant}/{self.policy}"
        client_application = PublicClientApplication(
            self.app_client_id,
            authority=authority,
            token_cache=self._create_encrypted_token_cache(),
        )

        b2c_tenant_url = f"https://{self.tenant}"
        scope = f"{b2c_tenant_url}/{self.api_client_id}/user_impersonation"
        api_scopes = [scope]

        auth_result: Optional[dict[str, Any]] = None

        # Have we got a cached sign-in?
        # See https://learn.microsoft.com/en-us/entra/identity-platform/scenario-desktop-acquire-token?tabs=python#recommended-pattern
        accounts = client_application.get_accounts()

        # If so, try to authenticate silently
        if accounts and len(accounts) > 0:
            auth_result = client_application.acquire_token_silent(
                scopes=api_scopes, account=accounts[0]
            )

        # Otherwise, authenticate interactively
        if not auth_result:
            auth_result = client_application.acquire_token_interactive(
                prompt=Prompt.SELECT_ACCOUNT, scopes=api_scopes, port=0
            )

        if auth_result and "error" in auth_result:
            print(
                f"Error: {auth_result['error']}."
                f"Error Description: {auth_result['error_description']}"
            )
            return auth_result

        return auth_result

    def renew_token(self, refresh_token: str) -> Optional[dict[str, Any]]:
        """
        Renews the access token using the provided refresh token.

        Args:
            refresh_token (str): The refresh token for token renewal.

        Returns:
            Optional[Dict[str, Any]]: The authentication results, typically including the
            access token, expiration time, etc.
        """

        # Please visit the link https://pypi.org/project/msal/ for implementation details

        authority = f"{self.authorization_endpoint}/{self.tenant}/{self.policy}"
        client_application = PublicClientApplication(
            self.app_client_id, authority=authority
        )

        b2c_tenant_url = f"https://{self.tenant}"
        scope = f"{b2c_tenant_url}/{self.api_client_id}/user_impersonation"
        api_scopes = [scope]

        auth_result = client_application.acquire_token_by_refresh_token(
            refresh_token, api_scopes
        )

        if "error" in auth_result:
            print(
                f"Error: {auth_result['error']}."
                f"Error Description: {auth_result['error_description']}"
            )
            return None

        return auth_result

    def _create_encrypted_token_cache(self):
        """
        Use the MSAL extensions to create an encrypted token cache
        that can only be accessed by the current user. This prevents
        the user being prompted to login every time.

        The token cache is protected using DPAPI on Windows, KeyChain on OSX
        and LibSecret on Linux.

        See https://github.com/AzureAD/microsoft-authentication-extensions-for-python
        """
        if self.cache:
            return self.cache

        cache_path = os.path.expanduser("~/.onecompute/tokencache.bin")
        persistence = build_encrypted_persistence(cache_path)
        self.cache = PersistedTokenCache(persistence)
        return self.cache


@dataclass
class MSALConfidentialClientAuthenticator(IAuthenticator):
    """
    This class provides a specialized token authenticator designed for confidential clients,
    including scenarios that involve service principals. It utilizes the Microsoft Authentication
    Library (MSAL).

    Attributes:
        authorization_endpoint (str): The authorization endpoint URL of the Azure AD B2C tenant.
        client_credential (str): A string containing client secret
        tenant (str): The Azure AD B2C tenant.
        app_client_id (str): The client ID of the application.
        scopes (List[str]): The list of scopes for authentication.
        auth_result (Optional[dict[str, Any]]): The optional authentication result.
    """

    authorization_endpoint: str
    client_credential: str
    tenant: str
    app_client_id: str
    scopes: list[str]
    auth_result: Optional[dict[str, Any]] = None

    def authenticate(self) -> Optional[dict[str, Any]]:
        """
        Performs the authentication process and returns the authentication results.

        Returns:
            Optional[Dict[str, Any]]: The authentication results, typically including the
            access token, expiration time, etc.
        """

        # Please visit the link https://pypi.org/project/msal/ for implementation details

        if self.auth_result:
            return self.auth_result

        authority = f"{self.authorization_endpoint}/{self.tenant}"
        client_application = ConfidentialClientApplication(
            client_id=self.app_client_id,
            authority=authority,
            client_credential=self.client_credential,
        )

        self.auth_result = client_application.acquire_token_for_client(
            scopes=self.scopes
        )

        if self.auth_result and "error" in self.auth_result:
            print(
                f"Error: {self.auth_result['error']}."
                f"Error Description: {self.auth_result['error_description']}"
            )
            return self.auth_result

        return self.auth_result

    def renew_token(self, refresh_token: str) -> Optional[dict[str, Any]]:
        """
        Renews the access token using the provided refresh token.

        Args:
            refresh_token (str): The refresh token for token renewal.

        Returns:
            Optional[Dict[str, Any]]: The authentication results, typically including the
            access token, expiration time, etc.
        """
        raise NotImplementedError("renew_token method is not implemented yet.")
