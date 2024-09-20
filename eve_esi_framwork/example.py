import logging
from base64 import b64encode

import requests as re
from django.conf import settings

logger = logging.getLogger(__name__)

token_url = 'https://login.eveonline.com/oauth/token'
verify_url = 'https://login.eveonline.com/oauth/verify'

auth = 'Basic ' + b64encode('{}:{}'.format(settings.CLIENT_ID, settings.CLIENT_SECRET).encode()).decode("utf-8")


def authorize(code):
    """
    Validate an authorization token recieved from

    :param code: client id and secret to authenticate with
    :return: json response
    """
    data = {
    'grant_type': 'authorization_code',
    'code': code,
    }

    r = re.post(token_url, json=data, headers={'Authorization': auth})
    if r.status_code != 200:
        logger.error('ESI request error: {} - {}'.format(r.status_code, r.content))
        raise Exception('Error authorizing')

    return r.json()


def verify(access_token, token_type):
    """
    Verifies the access token and retrieves character information

    :param auth: authorization header to be sent
    :return: character information
    """

    r = re.get(verify_url, headers={'Authorization': '{} {}'.format(token_type, access_token)})
    if r.status_code != 200:
        logger.error('ESI request error: {} - {}'.format(r.status_code, r.content))
        raise Exception('Error verifying character')

    return r.json()


def refresh(token_id, refresh_token):
    """
    Refresh expired access token.

    :param token_id: id for logging request errors
    :param refresh_token: refresh token associated with the expired access token
    :return: json response
    """
    data = {
    "grant_type": "refresh_token",
    "refresh_token": refresh_token
    }

    r = re.post(token_url, json=data, headers={'Authorization': auth})

    if r.status_code != 200:
        logger.error('Error refreshing token: {}\n'.format(token_id))
        raise Exception('Error refreshing token')

    return r.json()