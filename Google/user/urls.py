from django.urls import path
from .views import *

urlpatterns = [
   path("access/", drive_auth),
   path("list-files/", Drive_google_files.as_view()),
   path("remove-access/",Drive_logout.as_view())
]