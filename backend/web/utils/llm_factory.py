# llm_factory.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(override=True)

def get_llm(
    streaming: bool = None,
    bind_tools=None,
    extra_model_kwargs: dict = None,
    model: str = None,
    api_key: str = None,
    api_base: str = None
) -> ChatOpenAI:
    base_model = model or os.getenv("MODEL_NAME")
    key = api_key or os.getenv("API_KEY")
    base = api_base or os.getenv("API_BASE")
    stream = streaming if streaming is not None else True

    default_kwargs = {}
    # 重点：只有流式=True，才添加 stream_options
    if stream:
        default_kwargs["stream_options"] = {"include_usage": True}

    # 合并外部传入的额外参数
    if extra_model_kwargs is not None:
        default_kwargs.update(extra_model_kwargs)

    llm = ChatOpenAI(
        model=base_model,
        openai_api_key=key,
        openai_api_base=base,
        streaming=stream,
        model_kwargs=default_kwargs
    )
    if bind_tools is not None:
        llm = llm.bind_tools(bind_tools)
    return llm
