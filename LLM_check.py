from langchain_ollama import ChatOllama
llm = ChatOllama(model = 'llama3.2', tempertaure = 0)
response = llm.invoke("hello llm")
print(response)
print(response.content)