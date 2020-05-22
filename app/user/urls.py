from django.urls import path
from user.views import CreateUserView
from user.views import CreateTokenView
from user.views import ManageUserView


app_name = 'user'

urlpatterns = [
    path(
        'create/',
        CreateUserView.as_view(),
        name='create',
    ),
    path(
        'token/',
        CreateTokenView.as_view(),
        name='token',
    ),
    path(
        'me/',
        ManageUserView.as_view(),
        name='me',
    ),
]
