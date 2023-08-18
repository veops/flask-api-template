# -*- coding:utf-8 -*-


from functools import wraps

from flask import abort
from flask import current_app
from flask import request
from flask import session
from flask_login import login_user

from api.models.account import User


def _auth_with_session():
    if "acl" in session and "uid" in (session["acl"] or {}):
        user = User(session['acl']['uid'], session['acl'].get('username'), session['acl'].get('name'))
        login_user(user)
        return True
    return False


def _auth_with_ip_white_list():
    ip = request.remote_addr
    key = request.values.get('_key')
    secret = request.values.get('_secret')

    if not key and not secret and ip.strip() in current_app.config.get("WHITE_LIST", []):  # TODO
        user = User(0, 'worker', 'worker')
        login_user(user)
        return True
    return False


def auth_required(func):
    if request.get_json(silent=True) is not None:
        setattr(request, 'values', request.json)
    else:
        setattr(request, 'values', request.values.to_dict())

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        if _auth_with_session() or _auth_with_ip_white_list():
            return func(*args, **kwargs)

        abort(401)

    return wrapper


def auth_abandoned(func):
    setattr(func, "authenticated", False)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
