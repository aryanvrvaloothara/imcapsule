from datetime import datetime, timedelta

import jwt


SECRET_KEY = 'df780374ff614db313e455c50c60d931'


def generate_access_token(user):
    """
    Function that generates access token
    :param user: User object
    :return:
        token: JWT token with 6 hr life
    """
    payload = {
        'sub': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=360),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def generate_refresh_token(user):
    """
    Function that generates refresh token
    :param user: User object
    :return:
        token: JWT refresh token with 30 days life
    """
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token