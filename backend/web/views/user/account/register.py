from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from web.models.user import UserProfile

class RegisterView(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            confirm_password = request.data['confirm_password']

            if not username or not password or not confirm_password:
                return Response({
                    'result': '用户名或密码不能为空'
                })

            if User.objects.filter(username=username).exists():
                return Response({
                    'result': '用户名已存在，请修改'
                })

            if password != confirm_password:
                return Response({
                    'result': '两次密码输入不一致'
                })

            user = User.objects.create_user(username=username, password=password)
            userprofile = UserProfile.objects.create(user=user)
            refresh = RefreshToken.for_user(user) # 生成jwt

            response = Response ({
                'result': 'success',
                'access': str(refresh.access_token),
                'user_id': user.id,
                'username': username,
                'photo':userprofile.photo.url,
                'profile': userprofile.profile,
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

        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })