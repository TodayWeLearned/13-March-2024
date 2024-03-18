import ollama
import requests
import streamlit as st
from bs4 import BeautifulSoup

st.title('Dev.to Summarization')

url = st.text_input("Enter the URL of the dev.to article: ", placeholder="https://www.example.com")
level = st.selectbox("Select the audience level: ", ["Beginner", "Intermediate", "Expert"])

if 'stream' not in st.session_state:
    st.session_state['stream'] = ''
    
def stream_data(stream):
    for chunk in stream:
        yield chunk['message']['content']

def get_summary():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    article = soup.find(class_="crayons-article__body")
    messages = [
        {
            'role': 'user',
            'content': f'I want to summarize the key points and actions to take from the following article for an audience at level {level}, focusing on understanding the main idea. Article:\n\n{article.text}'
        }
    ]
    
    st.session_state.stream = ollama.chat(model='llama2:7b-chat', messages=messages, stream=True)
    
st.button("Summarize", type="primary", on_click=get_summary)

if st.session_state.stream is not "":
    st.subheader("Summary")
    st.write_stream(stream_data(st.session_state.stream))
