from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage

class MessagesState(MessagesState):
    #add msg
    pass

def tool_calling_llm(state:MessagesState):
    return {"messages": [llm_with_tool.invoke(state["messages"])]}

def add (a:int, b:int) -> int:
    """Add a and b"""
    return a+b

def multiply (a:int, b:int) -> int:
    """multiply a and b"""
    return a*b

def divide (a:int, b:int) -> int:
    """divide a by b"""
    return a/b

llm = ChatOpenAI(
    api_key = "ollama",
    model = "llama3.1:latest",
    base_url = "http://localhost:11434/v1"
)


llm_with_tool = llm.bind_tools([add, multiply, divide])

builder = StateGraph(MessagesState)
builder.add_node("tool", tool_calling_llm)
builder.add_edge(START,"tool")
builder.add_edge("tool", END)

graph = builder.compile()

#display graph
png_data = graph.get_graph().draw_mermaid_png()
with open("output.png", "wb") as f:
    f.write(png_data)

msg = {"messages":[HumanMessage(content="hello")]}

response = graph.invoke(msg)

for m in response["messages"]:
    m.pretty_print()
