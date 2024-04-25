#!/usr/bin/env python3
"""
Test script for API endpoints using requests.
"""

import requests


def register_user(email: str, password: str) -> None:
    """
    Test registration of a new user.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    resp = requests.post('http://127.0.0.1:5000/users',
                         data={'email': email, 'password': password})
    if resp.status_code == 200:
        assert (resp.json() == {"email": email, "message": "user created"})
    else:
        assert (resp.status_code == 400)
        assert (resp.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login with incorrect credentials.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    r = requests.post('http://127.0.0.1:5000/sessions',
                      data={'email': email, 'password': password})
    assert (r.status_code == 401)


def profile_unlogged() -> None:
    """
    Test profile access without logging in.

    Returns:
        None
    """
    r = requests.get('http://127.0.0.1:5000/profile')
    assert (r.status_code == 403)


def log_in(email: str, password: str) -> str:
    """
    Test login with correct credentials and return session ID.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID of the user.
    """
    resp = requests.post('http://127.0.0.1:5000/sessions',
                         data={'email': email, 'password': password})
    assert (resp.status_code == 200)
    assert (resp.json() == {"email": email, "message": "logged in"})
    return resp.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """
    Test profile access while logged in.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        None
    """
    cookies = {'session_id': session_id}
    r = requests.get('http://127.0.0.1:5000/profile',
                     cookies=cookies)
    assert (r.status_code == 200)


def log_out(session_id: str) -> None:
    """
    Test logout with session ID.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        None
    """
    cookies = {'session_id': session_id}
    r = requests.delete('http://127.0.0.1:5000/sessions',
                        cookies=cookies)
    if r.status_code == 302:
        assert (r.url == 'http://127.0.0.1:5000/')
    else:
        assert (r.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    Test generation of reset password token.

    Args:
        email (str): The email of the user.

    Returns:
        str: The reset token of the user.
    """
    r = requests.post('http://127.0.0.1:5000/reset_password',
                      data={'email': email})
    if r.status_code == 200:
        return r.json()['reset_token']
    assert (r.status_code == 401)


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """
    Test updating user's password.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset token of the user.
        new_password (str): The new password of the user.

    Returns:
        None
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put('http://127.0.0.1:5000/reset_password',
                     data=data)
    if r.status_code == 200:
        assert (r.json() == {"email": email, "message": "Password updated"})
    else:
        assert (r.status_code == 403)


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
