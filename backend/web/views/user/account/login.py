from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile


class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                Response({
                    'result': '用户名或者密码不能为空'
                })

            user = authenticate(username=username, password=password)
            if user:
                user_profile = UserProfile.objects.get(user=user)
                refresh = RefreshToken.for_user(user)  # 生成jwt
                response = Response({
                    'result': 'success',
                    'access': str(refresh.access_token),  #access返回给前端，refresh_token保留到cookies
                    'user_id': user.id,
                    'username': username,
                    'photo': user_profile.photo.url,  # 必须加url！！！
                    'profile': user_profile.profile,
                })
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    samesite='Lax',
                    secure=True,
                    max_age=86400 * 7,
                )
                return response
            return Response({
                'result': '用户名或者密码错误'
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })