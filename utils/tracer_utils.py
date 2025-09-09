import os
from langchain_core.tracers import LangChainTracer
from langchain_core.tracers.langchain import wait_for_all_tracers

def get_tracer():
    project = os.getenv("LANGCHAIN_PROJECT", "default-project")
    return LangChainTracer(project_name=project)

def wait_for_tracers():
    wait_for_all_tracers()
