"""Reusable Flask helpers for CodeVault.

This helper was drafted with AI assistance, then reviewed by the author.
"""

from functools import wraps

from flask import redirect, session, url_for


def login_required(view):
    """Redirect visitors to login unless they have an active user session."""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view
