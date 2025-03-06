from django.urls import path, include
from .views import google_login, google_callback
from user.views import drive_Callback


urlpatterns = [
    path("drive/", include("user.urls")),
    path("auth/google/signin/", google_login, name="google_login"),
    path("auth/google/callback/", google_callback, name="google_callback"),


    # path("google/drive_access/", get_google_drive_access),
    path("google/drive_access/callback/", drive_Callback),

    # path("list/files/", list_google_drive_files),
]
