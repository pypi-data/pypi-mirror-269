from cgc.utils.config_utils import read_from_cfg
from cgc.commands.auth import auth_utils
from cgc.utils.message_utils import key_error_decorator_for_helpers


def load_user_api_keys():
    """Based on configuration getter creates pair of API keys

    :return: api_key and api_secret
    :rtype: list of strings
    """
    return read_from_cfg("api_key"), read_from_cfg("api_secret")


def load_user_cgc_secret():
    return read_from_cfg("cgc_secret")


def load_user_api_url():
    return read_from_cfg("cgc_api_url")


@key_error_decorator_for_helpers
def get_api_url_and_prepare_headers():
    """Loads CGC_API_URL and user api keys into single function. Mend to be used as single point of truth for all endpoints except register - due to different Content-Type header

    :return: CGC_API_URL and headers
    :rtype: string and dict
    """
    api_key, api_secret = load_user_api_keys()
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json; charset=UTF-8",
        "comtegra-cgc": load_user_cgc_secret(),
        "api-key": api_key,
        "api-secret": api_secret,
    }
    return load_user_api_url(), headers


def get_url_and_prepare_headers_register(
    user_id: str, access_key: str, url: str = None, secret: str = None
):
    """Creates and returns url and headers for register request.

    :return: url, headers
    :rtype: string and dict
    """
    url = f"{load_user_api_url() if url is None else url}/v1/api/user/register?user_id={user_id}&access_key={access_key}"
    headers = {
        "accept": "application/json",
        "Content-Type": "octet-stream",
        "comtegra-cgc": load_user_cgc_secret() if secret is None else secret,
    }
    return url, headers


def get_url_and_headers_jwt_token():
    url = f"{load_user_api_url()}/v1/api/user/create/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    return url, headers


@key_error_decorator_for_helpers
def prepare_headers_api_key(user_id: str = None, password: str = None):
    """Prepares headers for create API key request.

    :return: headers in a for of dictionary
    :rtype: dict
    """
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {auth_utils.get_jwt(user_id, password)}",
        "comtegra-cgc": load_user_cgc_secret(),
    }
    return headers


def get_api_url_and_prepare_headers_version_control():
    """Prepares headers for version control request.

    :return: url and headers in a for of dictionary
    :rtype: string, dict
    """
    url = f"{load_user_api_url()}/v1/api/info/version"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "comtegra-cgc": load_user_cgc_secret(),
    }
    return url, headers
