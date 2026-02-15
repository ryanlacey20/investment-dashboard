from flask import Blueprint, redirect, request, jsonify, session
import requests
import base64
import secrets
import urllib.parse

from config import Config
from services.token_store import save_refresh_token, get_refresh_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def auth_already_completed():
    return get_refresh_token() is not None


@auth_bp.route("/login")
def login():

    if auth_already_completed():
        return "Authorization already completed.", 403

    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    redirect_uri_encoded = urllib.parse.quote(
        Config.SCHWAB_REDIRECT_URI, safe=""
    )

    auth_url = (
        f"{Config.SCHWAB_AUTH_URL}"
        f"?response_type=code"
        f"&client_id={Config.SCHWAB_CLIENT_ID}"
        f"&redirect_uri={redirect_uri_encoded}"
        f"&state={state}"
    )

    return redirect(auth_url)


@auth_bp.route("/callback")
def callback():

    if auth_already_completed():
        return "Authorization already completed.", 403

    code = request.args.get("code")
    state = request.args.get("state")

    if not code:
        return "Missing authorization code.", 400

    if not state or state != session.get("oauth_state"):
        return "Invalid state parameter.", 400

    credentials = f"{Config.SCHWAB_CLIENT_ID}:{Config.SCHWAB_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": Config.SCHWAB_REDIRECT_URI,
    }

    response = requests.post(
        Config.SCHWAB_TOKEN_URL,
        headers=headers,
        data=data,
        timeout=10
    )

    if response.status_code != 200:
        return "Token exchange failed.", 400

    tokens = response.json()

    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        return "No refresh token received.", 400

    save_refresh_token(refresh_token)

    session.pop("oauth_state", None)

    return "Authorization successful. You may close this window."
