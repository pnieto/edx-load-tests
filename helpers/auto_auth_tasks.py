import json
from locust import TaskSet

from helpers import settings

class AutoAuthTasks(TaskSet):
    """
    Methods useful to any/all tests that want to use auto auth.
    """

    def __init__(self, *args, **kwargs):
        """
        Add basic auth credentials to our client object when specified.
        """
        super(AutoAuthTasks, self).__init__(*args, **kwargs)

        basic_auth_credentials = (
          settings.data.get('BASIC_AUTH_USER', None),
          settings.data.get('BASIC_AUTH_PASS', None),
          )
        if basic_auth_credentials[0] is not None:
            self.client.auth = basic_auth_credentials

        self._user_id = None
        self._anonymous_user_id = None
        self._username = None
        self._email = None
        self._password = None

    def auto_auth(self, verify_ssl=True, params=None, hostname=''):
        """
        Logs in with a new, programmatically-generated user account.
        Requires AUTO_AUTH functionality to be enabled in the target edx instance.
        """
        if "sessionid" in self.client.cookies:
            del self.client.cookies["sessionid"]

        response = self.client.get(
            "{}/auto_auth".format(hostname),
            name="auto_auth",
            headers={'accept': 'application/json'},
            params=params or {},
            verify=verify_ssl
        )

        json_response = json.loads(response.text)
        self._username = json_response['username']
        self._email = json_response['email']
        self._password = json_response['password']
        self._user_id = json_response['user_id']
        self._anonymous_user_id = json_response['anonymous_id']
