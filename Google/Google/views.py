import requests
from django.http import JsonResponse
from django.shortcuts import redirect
import urllib.parse
from Google.settings import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI, GOOGLE_CLIENT_SECRET, GOOGLE_DRIVE_SCOPE


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": f"openid email profile {GOOGLE_DRIVE_SCOPE}",        
        "access_type": "offline",
        "prompt":"consent"
    }
    auth_url = f"{google_auth_url}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

def google_callback(request):
    code = request.GET.get("code")

    if code:
        data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        # Exchange auth code for access token
        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        tokens = response.json()

        if "access_token" in tokens:
            access_token = tokens["access_token"]

            # Fetch user info from Google
            user_info_response = requests.get(GOOGLE_USER_INFO_URL, headers={
                "Authorization": f"Bearer {access_token}"
            })
            user_info = user_info_response.json()
            print("user info: ", user_info)
            # Return user data from Google
            return JsonResponse(user_info)

    return JsonResponse({"error": "Authentication failed"}, status=400)
