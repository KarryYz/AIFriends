from django.urls import path, re_path

from web.views.create.character.get_single import GetSingleCharacterView
from web.views.create.character.remove import RemoveCharacterView
from web.views.index import index


from web.views.user.account.login import LoginView
from web.views.user.account.logout import LogoutView
from web.views.user.account.refresh_token import RefreshTokenView
from web.views.user.account.register import RegisterView
from web.views.user.account.get_user_info import GetUserInfoView
from web.views.user.profile.update import UpdateProfileView
from web.views.create.character.create import CreateCharacterView
from web.views.create.character.update import UpdateCharacterView

urlpatterns = [
    path('api/user/account/login/', LoginView.as_view(), name='login'),
    path('api/user/account/logout/', LogoutView.as_view(), name='logout'),
    path('api/user/account/register/', RegisterView.as_view(), name='register'),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view(), name='refresh'),
    path ('api/user/account/get_user_info/', GetUserInfoView.as_view(), name='get_user_info'),
    path ('api/user/profile/update/', UpdateProfileView.as_view(), name='update'),
    path('api/create/character/create/', CreateCharacterView.as_view(), name='create'),
    path('api/create/character/update/', UpdateCharacterView.as_view(), name='update'),
    path('api/create/character/remove/', RemoveCharacterView.as_view(), name='remove'),
    path('api/create/character/get_single/', GetSingleCharacterView.as_view(), name='get_single'),

    path('', index, name='index'),
    re_path(r'^(?!media/|static/|assets/).*$', index)
]
