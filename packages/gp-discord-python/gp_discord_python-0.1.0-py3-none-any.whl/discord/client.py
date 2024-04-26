import json
from urllib.parse import urlencode

import requests
from requests import Response

from discord import exceptions


class Client(object):
    BASE_URL = "https://discord.com"

    REQUEST_TOKEN = BASE_URL + "/api/v9/oauth2/token"
    REQUEST_AUTHORIZATION = BASE_URL + "/oauth2/authorize"
    CHANNELS = BASE_URL + "/api/guilds/{guild_id}/channels"
    MESSAGES = BASE_URL + "/api/channels/{channel_id}/messages"
    USER_INFO = BASE_URL + "/api/users/@me"

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.access_token = None
        self.bot_token = None
        self.token = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = ""
        self.scopes = []

    def authorization_url(self, redirect_uri: str) -> str:
        self.redirect_uri = redirect_uri
        params = {
            "client_id": self.client_id,
            "permissions": "8",
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": "+".join(self.scopes),
        }
        url = self.REQUEST_AUTHORIZATION + "?" + urlencode(params).replace("%2B", "+")
        return url

    def exchange_code(self, code: str) -> Response:
        """ Exchange code
        Args:
            code (str): _description_

        Returns:
            Response: _description_
        """
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
        }
        response = self._post(self.REQUEST_TOKEN, data=data, no_header={})
        return response

    def refresh_token(self, refresh_token: str) -> Response:
        """ Refresh token access
        Args:
            refresh_token (str): _description_

        Returns:
            Response: _description_
        """
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response = self._post(self.REQUEST_TOKEN, data=data)
        return response

    def set_access_token(self, token: str) -> None:
        """Sets the access_token for its use in this library.
        Args:
            token (str): access_token data.
        """
        self.token = "Bearer " + token

    def set_bot_token(self, token: str) -> None:
        """Sets the access_token for its use in this library.
        Args:
            token (str): access_token data.
        """
        self.token = f"Bot {token}"

    def get_by_url(self, url: str) -> Response:
        """Get data from any url.
        Args:
            url (str): Url to get data

        Returns:
            Response: dict request data
        """
        response = self._get(url=url)
        return response

    def get_user_info(self) -> Response:
        """User info from Discord Api.

        Returns:
            Response: dict of user info
        """
        response = self._get(url=self.USER_INFO)
        return response

    def get_channel_list(self, guild_id) -> Response:
        """List of channels from Discord API.
        Args:
            guild_id (str): ID of guild given from Oauth

        Returns:
            Response: dict of channels
        """
        response = self._get(url=self.CHANNELS.format(guild_id=guild_id))
        return response

    def get_messages(self, channel_id: str) -> Response:
        """Get messages from Discord API

        Args:
            channel_id (str): ID of channel in Discord

        Returns:
            Response: dict of messages
        """
        response = self._get(url=self.MESSAGES.format(channel_id=channel_id))
        return response

    def send_messages(self, channel_id: str, data: json) -> Response:
        """Send message through Discord API.

        Args:
            channel_id (str): ID of channel in Discord
            data (json): data to send

        Returns:
            Response: dict of messages
        """
        response = self._post(
            url=self.MESSAGES.format(channel_id=channel_id), data=data
        )
        return response

    def _get(self, url, **kwargs) -> Response:
        response = self._do_get(url, **kwargs)
        return response

    def _do_get(self, url, **kwargs) -> Response:
        return self._request("GET", url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request("POST", url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request("PUT", url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._request("PATCH", url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request("DELETE", url, **kwargs)

    def _request(self, method, url, **kwargs) -> Response:
        if "no_header" in kwargs:
            _headers = kwargs.pop("no_header")
        else:
            _headers = {"Authorization": self.token, "Content-Type": "application/json"}

        return self._parse(requests.request(method, url, headers=_headers, **kwargs))

    def _parse(self, response) -> Response:
        status_code = response.status_code

        if (
            "Content-Type" in response.headers
            and "application/json" in response.headers["Content-Type"]
        ):
            r = response.json()
        else:
            r = response.content

        if status_code in (200, 201, 202, 204, 206):
            return r
        elif status_code == 400:
            raise exceptions.BadRequest(r)
        elif status_code == 401:
            raise exceptions.Unauthorized(r)
        elif status_code == 403:
            raise exceptions.Forbidden(r)
        elif status_code == 404:
            raise exceptions.NotFound(r)
        elif status_code == 405:
            raise exceptions.MethodNotAllowed(r)
        elif status_code == 406:
            raise exceptions.NotAcceptable(r)
        elif status_code == 409:
            raise exceptions.Conflict(r)
        elif status_code == 410:
            raise exceptions.Gone(r)
        elif status_code == 411:
            raise exceptions.LengthRequired(r)
        elif status_code == 412:
            raise exceptions.PreconditionFailed(r)
        elif status_code == 413:
            raise exceptions.RequestEntityTooLarge(r)
        elif status_code == 415:
            raise exceptions.UnsupportedMediaType(r)
        elif status_code == 416:
            raise exceptions.RequestedRangeNotSatisfiable(r)
        elif status_code == 422:
            raise exceptions.UnprocessableEntity(r)
        elif status_code == 429:
            raise exceptions.TooManyRequests(r)
        elif status_code == 500:
            raise exceptions.InternalServerError(r)
        elif status_code == 501:
            raise exceptions.NotImplemented(r)
        elif status_code == 503:
            raise exceptions.ServiceUnavailable(r)
        elif status_code == 504:
            raise exceptions.GatewayTimeout(r)
        elif status_code == 507:
            raise exceptions.InsufficientStorage(r)
        elif status_code == 509:
            raise exceptions.BandwidthLimitExceeded(r)
        else:
            if r["error"]["innerError"]["code"] == "lockMismatch":
                raise exceptions.ServiceUnavailable(r)
            raise exceptions.UnknownError(r)
