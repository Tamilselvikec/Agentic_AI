#openai wrapper for ollama
from langchain_openai import ChatOpenAI

#define tool

def add(a: int, b:int) -> int:
    """
    arg: a,b
    """
    return a + b


llm = ChatOpenAI(
    api_key = "ollama",
    model = "llama3.1:latest",
    base_url = "http://localhost:11434/v1"
)

#check LLM working status
print(llm.invoke("hello"))

print("---------------------------------------------------------------------")

llm_with_tool = llm.bind_tools([add])

response = llm_with_tool.invoke("Add 2 and 3")
print(response) # check additional_kwargs - should not be empty for tool call

print("---------------------------------------------------------------------")
resp = llm_with_tool.invoke("hi")
print(resp)