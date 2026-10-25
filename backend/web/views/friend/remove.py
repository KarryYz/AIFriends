from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.friend import Friend


class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            friend_id = request.data['friend_id']
            Friend.objects.filter(pk=friend_id, me__user=request.user).delete()
            return Response({
                'status': 'success',
            })
        except:
            return Response ({
                'result': '系统异常，请稍后重试'
            })