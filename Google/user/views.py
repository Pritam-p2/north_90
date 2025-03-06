from google_auth_oauthlib.flow import Flow
from rest_framework.views import APIView
from Google.settings import CLIENT_SECRETS_FILE, GOOGLE_DRIVE_SCOPE
from rest_framework.response import Response
from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.decorators import api_view

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=GOOGLE_DRIVE_SCOPE,
    redirect_uri="http://localhost:8000/google/drive_access/callback/"
)


def credentials_to_dict(credentials):
    """Convert OAuth credentials to a dictionary."""
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


@api_view(["GET"])
def drive_auth(request):
    if not request.user.is_authenticated:
        return Response({'error':'Authentication requied'}, status=400)

    auth_url, _ = flow.authorization_url(prompt="consent")
    return Response({"auth_url": auth_url})


@api_view(["GET"])
def drive_Callback(request):
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    request.session["credentials"] = credentials_to_dict(credentials)

    return redirect("/list-files/")


class Drive_google_files(APIView):
    def get(request):
        if "credentials" not in request.session:
            return Response({"error": "User not authenticated"}, status=401)

        credentials = Credentials(**request.session["credentials"])
        drive_service = build("drive", "v3", credentials=credentials)

        results = drive_service.files().list(
            pageSize=10, fields="files(id, name, mimeType)"
        ).execute()

        return Response(results.get("files", []))
    
class Drive_logout(APIView):
    def get(request):
        request.session.flush()
        return Response({"message": "Logged out successfully"})