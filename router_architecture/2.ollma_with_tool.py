from langchain_ollama import ChatOllama


#define a tool

def add (a:int, b:int) -> int:
    """
    Arg: a, b
    """
    return a + b

#Define LLM
llm = ChatOllama(
    model = "llama3.1:latest"
)

#Bind LLM with tool

llm_with_tool = llm.bind_tools([add]) #bind_tools takes list of tools

resp = llm_with_tool.invoke("add 2 and 3")
print(resp)

print("----------------------------------------------------------------------")

# with ollama capability, binding is not done properly
# In resp check additional_kwargs - it will be {} (issue here) - make openai warpper for ollama
# content should be empty when calling tool because LLM should not generate any o/p, tool has to generate o/p

resp = llm_with_tool.invoke("hello")
print(resp)
#check content - non-empty, additional_kwargs should {}

