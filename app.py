import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain_community.llms import ollama
from langchain_ollama.llms import OllamaLLM
#Prompt Template
prompt=ChatPromptTemplate.from_messages([
    ('system','you are a helpful assitant. please response to the user queries'),
    ('user','Question:{question}')
])

def generate_response(api_key,engine,question):
    if engine in ['gpt-4o','gpt-4-turbo','gpt-4']:
        model=ChatOpenAI(model=engine,api_key=api_key)
    elif engine not in ['gpt-4o','gpt-4-turbo','gpt-4']:
        model=OllamaLLM(model=engine)    
    chain=prompt|model|StrOutputParser()
    answer=chain.invoke(input={'question':question})
    return answer

# Title of the App
st.title('Q&A Chatbot Using OpenAI and Ollama')

# Sidebar settings
st.sidebar.title('Settings')

# Enter API key and Select the model
engine=st.sidebar.selectbox('Select the Model:',['gpt-4o','gpt-4-turbo','gpt-4','gemma2:2b'])
if engine in ['gpt-4o','gpt-4-turbo','gpt-4']:
    api_key=st.sidebar.text_input('Enter API key:',type="password")
else:
    api_key=None    


st.write('Go ahead and ask the question')
user_input=st.text_input('You:')

if user_input and engine:
    response=generate_response(api_key=api_key,engine=engine,question=user_input)
    st.write(response)
elif not user_input:
    st.write('Please provide the question')    
elif not api_key and engine in ['gpt-4o','gpt-4-turbo','gpt-4']:
    st.write('provide a valid api key')    
elif not engine:
    st.write('Select the model')    
