import json

from django.http import StreamingHttpResponse
from langchain_core.messages import HumanMessage, BaseMessageChunk, SystemMessage, AIMessage
from rest_framework.renderers import BaseRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend, Message, SystemPrompt
from web.views.friend.message.chat.graph import ChatGraph


class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


def add_system_prompt(state, friend):
    msgs = state['messages']
    system_prompts = SystemPrompt.objects.filter(title='回复' ).order_by('order_number')
    prompt = ''
    for sp in system_prompts:
        prompt += sp.prompt
    prompt = f"\n【角色性格】 \n{friend.character.profile} \n"
    return {'messages': [SystemMessage(prompt)] + msgs}



def add_recent_message(state, friend):
    msgs = state['messages']
    message_raw = list (Message.objects.filter(friend=friend).order_by('-id')[:10])
    message_raw.reverse()

    messages = []
    for m in message_raw:
        messages.append(HumanMessage(m.user_message))
        messages.append(AIMessage(m.output))

    return {'messages': msgs[:1] + messages + msgs[-1:]}


class MessageChatView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]

    def post(self, request):
        friend_id = request.data.get('friend_id')
        message = request.data.get('message').strip()

        if not message:
            return Response({
                'result': '消息不能为空'
            })

        friends = Friend.objects.filter(pk=friend_id, me__user=request.user)
        if not friends.exists():
            return Response({
                'result': '好友不存在'
            })

        friend = friends.first()
        app = ChatGraph.create_app()

        inputs = {
            'messages': [HumanMessage(message)] #和构造的函数内变量名对应，封装传入的消息
        }

        inputs = add_system_prompt (inputs, friend)
        inputs = add_recent_message (inputs, friend)

        # res = app.invoke(inputs)  # 调用计算流程
        # print(res['messages'][-1].content)  # 会返回一个

        # 流式回复： yield：生成器，每执行一次，会往下进行一个yield之前的内容；
        # 生成器定义
        def event_stream():
            full_output = ''
            full_usage = {}  # 存储消耗量
            for msg, metadata in app.stream(inputs, stream_mode="messages"):
                if isinstance(msg, BaseMessageChunk):  # 消息是否是本次片段
                    if msg.content:  # 判断是否有消息
                        full_output += msg.content
                        yield f"data:{json.dumps({'content': msg.content}, ensure_ascii=False)}\n\n"  # ensure_ascii=False 确保返回为unicode 看中文
                    if hasattr(msg, 'usage_metadata') and msg.usage_metadata:  # 存储usage信息
                        full_usage = msg.usage_metadata
            yield 'data: [DONE]\n\n'  # 结束格式 data: [DONE]\n\n

            input_tokens = full_usage.get ('input_tokens', 0)
            output_tokens = full_usage.get ('output_tokens', 0)
            total_tokens = full_usage.get ('total_tokens', 0)

            Message.objects.create(
                friend=friend,
                user_message=message,
                input=json.dumps(
                    [m.model_dump() for m in inputs['messages']],
                    ensure_ascii=False,  # 保证输出的是中文而不是unicode
                )[:10000],  # 截断，长度和web/models/friend.py Message中定义的一致
                output=full_output[:500],
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
            )

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")  # 返回StreamingHttpResponse
        response['Cache-Control'] = 'no-cache'

        return response