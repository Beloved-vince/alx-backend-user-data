#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """register_user method
    """
    payload = {'email': email, 'password': password}
    res = requests.post('http://0.0.0.0:5000/users', data=payload)

    assert res.status_code == 200
    assert res.json() == {"email": "{}".format(email),
                          "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """log_in_method
    """
    payload = {'email': email, 'password': password}
    res = requests.post('http://0.0.0.0:5000/sessions', data=payload)
    assert res.status_code == 401


def profile_unlogged() -> None:
    """profile
    """
    res = requests.get('http://0.0.0.0:5000/profile')
    assert res.status_code == 403


def log_in(email: str, password: str) -> str:
    """log_in
    """
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5'
    payload = {'email': email, 'password': password}

    response = session.post('http://0.0.0.0:5000/sessions', data=payload)
    cookieJar = session.cookies
    assert response.status_code == 200
    assert response.json() == {"email": "{}".format(
        email), "message": "logged in"}
    return cookieJar.get('session_id')


def profile_logged(session_id: str) -> None:
    """profile_logged
    """
    session = requests.Session()
    session.cookies['session_id'] = session_id
    res = session.get('http://0.0.0.0:5000/profile')

    assert res.json() == {"email": "{}".format(EMAIL)}


def log_out(session_id: str) -> None:
    """logout
    """
    session = requests.Session()
    session.cookies['session_id'] = session_id
    res = session.delete('http://0.0.0.0:5000/sessions')

    assert res.url == "http://0.0.0.0:5000/"


def reset_password_token(email: str) -> str:
    """reset password
    """
    payload = {'email': email}
    res = requests.post('http://0.0.0.0:5000/reset_password', data=payload)
    assert res.status_code == 200
    token = res.json()
    return token["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update paswword
    """
    payload = {'reset_token': reset_token,
               "new_password": new_password, "email": email}
    res = requests.put('http://0.0.0.0:5000/reset_password', data=payload)
    assert res.status_code == 200
    assert res.json() == {"email": "{}".format(
        email), "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)