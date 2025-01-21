#simple graph
'''
                        Node 2
START ----> Node 1 --->         -----> END
                        Node 3
'''

# 3 nodes, 1 conditional edge

# Steps
# 1. Define the state of the graph - state schema serves as input schema for all nodes and edges in graph
# 2. Define Nodes - Nodes are python functions. Each node operates on state, override previous state value
# 3. Define edges - which connects nodes - two types of edges (normal, conditional edges).
#    Conditional edges is implemented as function that returns next node to be visited based on some logic
# 4. Construct graph
# 5. Invoke the graph


from typing import TypedDict, Literal
import random
from langgraph.graph import  StateGraph, START, END


# define state
class State(TypedDict):
    graph_state: str

# Define 3 node
def node_1(state):
    print("------In Node 1-----")
    return {"graph_state": state['graph_state'] + "HI_"}

def node_2(state):
    print("------In Node 2-----")
    return {"graph_state": state['graph_state'] + "INFOSYS"}

def node_3(state):
    print("------In Node 3-----")
    return {"graph_state": state['graph_state'] + "AGENT"}

# function for conditional edge
def decision_node(state) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"

    return "node_3"

# construct graph
builder = StateGraph(State) #Intialize StateGraph with State
builder.add_node("node_1",node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decision_node)
builder.add_edge("node_2", END)
builder.add_edge("node_3",END)

graph = builder.compile()


# Save the PNG image to a file
png_data = graph.get_graph().draw_mermaid_png()
with open("output.png", "wb") as f:
    f.write(png_data)


#Graph invocation
response = graph.invoke({'graph_state':"hello_"})
print(response)









