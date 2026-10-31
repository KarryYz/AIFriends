import os
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph

from web.utils.llm_factory import get_llm


class MemoryGraph:
    @staticmethod
    def create_app ():
        llm = get_llm(
            streaming=False,
        )

        class AgentState(TypedDict):  # 数据类型
            messages: Annotated[Sequence[BaseMessage], add_messages]

        def model_call(state: AgentState) -> AgentState:
            res = llm.invoke(state['messages'])  # 调用大模型
            return {'messages': [res]}


        graph = StateGraph (AgentState)
        graph.add_node('agent', model_call)

        graph.add_edge(START, 'agent')
        graph.add_edge( 'agent', END)

        return graph.compile()