# Internal nodes pass some information that may not be needed in graph input/output

# separate schema for input, output, overall state

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# class Entirestate(TypedDict):
#     visit_count: int
#
# class Privatestate(TypedDict):
#     intermediate_count: int
#
# def node_1(state:Entirestate) -> Privatestate:
#     return {
#         "intermediate_count": state['visit_count'] + 1
#     }
#
# def node_2(state:Privatestate) -> Entirestate:
#     return{
#         "visit_count": state['intermediate_count'] + 1
#     }
#
# builder = StateGraph(Entirestate)
#
# builder.add_node("node_1", node_1)
# builder.add_node("node_2", node_2)
#
# builder.add_edge(START, "node_1")
# builder.add_edge("node_1", "node_2")
# builder.add_edge("node_2", END)
#
# graph = builder.compile()
#
# res = graph.invoke({
#     "visit_count": 233
# })
#
# print(res)

# ------------------------------------------------------------------

# StateGraph takes in a single schema and all nodes are expected to communicate with that schema.
# define explicit input and output schemas for a graph
# class overall_schema(TypedDict):
#     question: str
#     answer: str
#     intermediate_answer: str
#
# def thinking_node(state: overall_schema):
#
#     return{
#         "intermediate_answer": "7+4 = 11, answer is 11",
#         "answer": "answer is 11"
#     }
#
#
# def answer_node(state: overall_schema):
#     return{
#         "answer": "answer is 11"
#     }
#
# builder = StateGraph(overall_schema)
#
# builder.add_node("thinking_node", thinking_node)
# builder.add_node("answer_node", answer_node)
#
# builder.add_edge(START,"thinking_node")
# builder.add_edge("thinking_node","answer_node")
# builder.add_edge("answer_node", END)
#
# graph = builder.compile()
#
# res = graph.invoke({
#     "question": "what is 7+4"
# })
#
# print(res)

#-----------------------------------------------------------------------

#Filter by input and output schema

class overall_schema(TypedDict):
    question: str
    answer: str
    intermediate_answer: str

class input_schema(TypedDict):
    question: str

class output_schema(TypedDict):
    answer: str

def thinking_node(state: overall_schema):

    return{
        "intermediate_answer": "7+4 = 11, answer is 11",
        "answer": "answer is 11"
    }


def answer_node(state: overall_schema):
    return{
        "answer": "answer is 11"
    }

builder = StateGraph(
    overall_schema,
    input = input_schema,
    output = output_schema
)

builder.add_node("thinking_node", thinking_node)
builder.add_node("answer_node", answer_node)

builder.add_edge(START,"thinking_node")
builder.add_edge("thinking_node","answer_node")
builder.add_edge("answer_node", END)

graph = builder.compile()

res = graph.invoke({
    "question": "what is 7+4"
})

print(res)
