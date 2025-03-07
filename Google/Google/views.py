import requests
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.response import Response
import urllib.parse
from Google.settings import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI, GOOGLE_CLIENT_SECRET, GOOGLE_TOKEN_URL, GOOGLE_USER_INFO_URL, GOOGLE_AUTH_URL
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from django.contrib.auth.hashers import make_password

def google_login(request):
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt":"consent"
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

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

        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        tokens = response.json()

        if "access_token" in tokens:
            access_token = tokens["access_token"]


            user_info_response = requests.get(GOOGLE_USER_INFO_URL, headers={
                "Authorization": f"Bearer {access_token}"
            })
            user_info = user_info_response.json()
            user,created = User.objects.get_or_create(email=user_info['email'], name = user_info['name'])
            if created:
                user.password = make_password('password')
                user.save()
            tokens = get_tokens_for_user(user)
            tokens.pop('refresh')
            return JsonResponse(tokens, status= status.HTTP_200_OK)
            
         

    return JsonResponse({"error": "Authentication failed"}, status=400)


# def get_google_drive_access(request):
#     params = {
#         "client_id": GOOGLE_CLIENT_ID,
#         "redirect_uri": GOOGLE_REDIRECT_URI,
#         "response_type": "code",
#         "scope": GOOGLE_DRIVE_SCOPE,
#         "access_type": "offline",
#         "prompt": "consent"
#     }
#     auth_url = f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"
#     print("running")
#     return redirect(auth_url)


# def google_callback_drive(request):
#     if not request.user.is_authenticated:
#         return Response({'error':'Authentication requied'}, status=400)
#     print(request.user.is_authenticated)
#     code = request.GET.get("code")
#     token_data = {
#         "code": code,
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "redirect_uri": GOOGLE_REDIRECT_URI,
#         "grant_type": "authorization_code",
#     }
#     response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
#     tokens = response.json()
#     request.user.access = tokens.get("access_token")
#     request.user.refresh = tokens.get("refresh_token")
#     request.user.save()

#     return Response(status=status.HTTP_201_CREATED)

# def upload_to_google_drive(request):
#     if request.method == "POST" and request.FILES.get("file"):
#         file = request.FILES["file"]

#         # Get user's access token
#         access_token = request.user.google_access_token

#         headers = {
#             "Authorization": f"Bearer {access_token}",
#         }

#         files = {
#             "file": (file.name, file.read(), file.content_type),
#         }

#         metadata = {
#             "name": file.name,
#         }

#         response = requests.post(
#             "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
#             headers=headers,
#             files=files,
#             data=metadata,
#         )

#         return JsonResponse(response.json(), safe=False)

#     return JsonResponse({"error": "Invalid request"}, status=400)

# def list_google_drive_files(request, access_token):
#     user = request.user
#     if user.
#     access_token = user.access
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#     }
#     response = requests.get(
#         GOOGLE_FILES_URL,
#         headers=headers
#     )

#     return JsonResponse(response.json(), safe=False)