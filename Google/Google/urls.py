from django.urls import path, include
from .views import google_login, google_callback

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("auth/google/signin/", google_login, name="google_login"),
    path("auth/google/callback/", google_callback, name="google_callback"),
]

# client secret
# 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

# client id
# 817203850416-vspdda44e1piv8t34i9eqmrjloh9p5uc.apps.googleusercontent.com

# policy
# https://chatgpt.com/canvas/shared/67c69d05dc408191bcb66763e8381552


# https://localhost:8000/privacy_policy/

# google picker api key
# AIzaSyAnWWn1YC9yy-8ctZNQlbRvJkgEL8Uv0ZA