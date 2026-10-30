import os
from typing import TypedDict, Annotated, Sequence

from django.utils.timezone import localtime, now
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode


class ChatGraph:
    @staticmethod
    def create_app ():
        @tool
        def get_time() -> str:
            """当需要查询精确时间时，调用此函数。返回格式为：[年-月-日 时:分:秒]"""
            return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')

        tools = [get_time]

        # 1.初始化大模型对象，对接deepseek
        llm = ChatOpenAI(
            model="deepseek-flash",
            openai_api_key = os.getenv('API_KEY'), #从环境变量读取密钥
            openai_api_base = os.getenv('API_BASE'), #deepseek接口地址
            streaming = True,  # 流式输出
            model_kwargs = {
                "stream_options": {
                    "include_usage": True,  # 输出token消耗数量
                }
            }
        ).bind_tools(tools)

        # 2.定义AgentState：图的状态（全局存储，整个graph流程共享的数据）
        class AgentState(TypedDict):
            # messages：消息列表，保存历史对话
            # Annotated：给字段加注解；add_messages是langgraph内置reducer
            # add_messages作用：新的消息不会覆盖旧列表，而是追加到列表尾部
            messages: Annotated[Sequence[BaseMessage], add_messages]

        # 3.定义图节点函数：真正调用大模型的业务逻辑
        def model_call(state: AgentState) -> AgentState:
            # state["messages"]拿到当前状态里全部历史消息，传给大模型
            res = llm.invoke(state["messages"])
            # 返回新消息，add_messages会自动把res追加到messages列表，不是覆盖
            return {
                'messages': [res]
            }

        def should_continue(state: AgentState) -> str:
            last_message = state['messages'][-1]
            if last_message.tool_calls:
                return "tools"
            return "end"

        tool_node = ToolNode(tools)

        # 4.构建状态图
        graph = StateGraph(AgentState) #指定这个图使用的状态类型
        graph.add_node('agent', model_call) #注册节点，名字叫agent，执行model_call函数
        graph.add_node('tools', tool_node)

        # 5.设置边（流转关系）
        graph.add_edge(START, 'agent') #流程起点START → 走到agent节点
        # graph.add_edge('agent', END) #agent执行完直接走到END，结束流程
        graph.add_conditional_edges(
            'agent',
            should_continue,
            {
                'tools': 'tools',
                'end': END,
            }
        )
        graph.add_edge('tools', 'agent')

        return graph.compile() #编译图，返回可调用的app对象
