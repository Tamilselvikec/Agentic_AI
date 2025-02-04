# same as file 5.simple_chain_with_langgraph
# to get result add ToolNode and conditional edge


from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode, tools_condition

class MessagesState(MessagesState):
    #add msg
    pass


def tool_calling_llm(state:MessagesState):
    # print(state['messages'])
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
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools",ToolNode([add,multiply,divide]))
builder.add_edge(START,"tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools", END)





graph = builder.compile()

#display graph
png_data = graph.get_graph().draw_mermaid_png()
with open("output.png", "wb") as f:
    f.write(png_data)



response = graph.invoke({"messages":[HumanMessage(content="add 2 and 3, then multiply by 2 ,then divide by 2")]})

for m in response["messages"]:
    m.pretty_print()