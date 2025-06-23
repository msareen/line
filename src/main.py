# basic imports
import os
from dotenv import load_dotenv
import traceback

# typing imports
from typing import Annotated
from typing_extensions import TypedDict

# LangGraph imports
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

# memory imports
from langgraph.checkpoint.memory import MemorySaver

# tool Imports
from langgraph.prebuilt import ToolNode, tools_condition

# My basic Tools 
from tools.local_tools import get_local_tools
from langgraph.types import Command


load_dotenv()



config = {"configurable": {"thread_id": "1"}}

os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")

llm = init_chat_model("google_genai:gemini-2.0-flash")

llm_with_tools = llm.bind_tools(get_local_tools())

isInterrupt = False

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    interrupt_is_set: bool


graph_builder = StateGraph(State)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}



def stream_graph_updates(user_input: str, is_user_command: bool = False):
    global isInterrupt
    human_command = None
    state = None
    if(is_user_command):
        human_command = Command(resume={"data": user_input})
        isInterrupt = False
    else: 
        state: State = {
            "messages": [
                {"role": "user", "content": user_input}
            ],
            "interrupt_is_set": False
        }
    events = graph.stream(
        human_command or state,
        config,
        stream_mode="values",
    )
    for event in events:
        if "__interrupt__" in event:
            isInterrupt = True
        if "messages" in event:
            event["messages"][-1].pretty_print()
       



# building the graph
tool_node = ToolNode(get_local_tools())

graph_builder.add_edge(START, "chatbot")
graph_builder.add_node("chatbot", chatbot)

# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {
        "tools": "tools", 
        END: END
    }
)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge("tools", "chatbot")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)



def main():
    try:
        with open("graph.png", "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())
    except Exception:
        # This requires some extra dependencies and is optional
        pass
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input, is_user_command=isInterrupt)
        except:
            print("An error occurred:")
            traceback.print_exc()
            break

if __name__ == "__main__":
    main()
