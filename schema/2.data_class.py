# schema - structure and types of data used by graph - all nodes communicate with that schema

from typing import TypedDict, Literal
from dataclasses import dataclass
import random
from langgraph.graph import StateGraph, START, END


@dataclass
class my_schema:
    name: str
    org: Literal["AAA", "BBB"]
    age: int

def node_1(state):
    print("I am in node 1.....")
    return {"name": state.name}

def node_2(state):
    print("I amin node 2.....")
    return {"org":"AAA"}

def node_3(state):
    print("I amin node 3.....")
    return {"org":state.org}

def node_4(state):
    print("I amin node 4.....")
    return {"age": state.age}

def decide_org(state) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"
    else:
        return "node_3"

builder = StateGraph(my_schema)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_node("node_4", node_4)

builder.add_edge(START,"node_1")
builder.add_conditional_edges("node_1",decide_org)
builder.add_edge("node_2","node_4")
builder.add_edge("node_3","node_4")
builder.add_edge("node_4", END)

graph = builder.compile()


png_data = graph.get_graph().draw_mermaid_png()
with open("output.png", "wb") as f:
    f.write(png_data)



res = graph.invoke(my_schema(name="XAE", age= 40, org="AAA"))
print(res)

res = graph.invoke(my_schema(name="XAE", age= 40, org="CCC"))
print(res)