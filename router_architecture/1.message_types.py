from langchain_core.messages import HumanMessage,AIMessage,SystemMessage,ToolMessage
from langchain_ollama import ChatOllama

#Langchain messages should be list

msg = [HumanMessage(content="Hello", name = 'user_1')]

llm = ChatOllama(
    model = "llama3.1:latest"
)

response = llm.invoke(msg)
# other format: response = llm.invoke("hello")
# invoke() accepts str/list of str


print(response) #entire response
print(response.content) # Only LLM generated response
print(type(response)) # response is of type AI message

