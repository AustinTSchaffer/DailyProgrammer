r"""

Contains the Recipient class, which encapsulates calls to the
recipient's HTTP endpoint(s).

"""

import requests


class Recipient(object):
    """
    Wraps HTTP calls to the recipient's REST endpoint.
    """

    def __init__(self, base_url: str, username: str, password: str):
        self._base_url = base_url
        self._username = username
        self._password = password

    def upload(self, event_data: dict) -> dict:
        """
        Uploads event data to the recipient's endpoint and resurns the parsed
        JSON response as a dict.
        """

        resp = requests.post(
            self._base_url,
            headers={"Content-Type": "application/json"},
            json=event_data,
            auth=(self._username, self._password),
        )

        assert resp.ok, resp.text
        return resp.json()
