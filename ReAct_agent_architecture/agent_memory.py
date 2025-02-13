from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState, StateGraph, START
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.checkpoint.memory import MemorySaver

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# This will be a tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

def assistant(state:MessagesState):
    return {"messages":[llm_with_tools.invoke([sys_msg] + state["messages"])]}

sys_msg = SystemMessage(content = "You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

llm = ChatOpenAI(
    api_key = "ollama",
    model = "llama3.1:latest",
    base_url = "http://localhost:11434/v1"
)


tools = [add, multiply, divide]
llm_with_tools = llm.bind_tools(tools,parallel_tool_calls=False)

builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START,"assistant")
builder.add_conditional_edges("assistant",tools_condition)
builder.add_edge("tools","assistant")


memory = MemorySaver()
react_graph_with_memory = builder.compile(checkpointer=memory)

# Each run of graph results in checkpoint when used with memory
# Thread is a collection of checkpoints
config = {
    "configurable": {"thread_id":1}
}

messages = [HumanMessage(content = "Add 2 and 3")]

response = react_graph_with_memory.invoke(
    {
        "messages": messages
    },
    config
)

for m in response['messages']:
    m.pretty_print()



messages = [HumanMessage(content = "Add again 2 to it")]

response = react_graph_with_memory.invoke(
    {
        "messages": messages
    },
    config
)

for m in response['messages']:
    m.pretty_print()

