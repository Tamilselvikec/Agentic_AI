from langchain_openai import ChatOpenAI

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

#LLM check
print(llm.invoke("hi"))
print("----------------------------------------------------------------")

llm_with_tool = llm.bind_tools([add, multiply, divide])

# print(llm_with_tool.invoke("add 2 and 3")) # 1 tool call

print("----------------------------------------------------------------")

print(llm_with_tool.invoke("add 2 and 3 then multiply by 4"))
# 2 tool call observe additional_kwargs of output