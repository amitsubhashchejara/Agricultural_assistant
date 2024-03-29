import streamlit as st
import os
import google.generativeai as gemini
import textwrap

google_palm_api= st.secrets["GEMINI_API"]

gemini.configure(
    api_key=google_palm_api)

model = gemini.GenerativeModel('gemini-pro')

def to_markdown(text):
  text = text.replace('•', '  *')
  text = text.replace('*', '')
  return ((textwrap.indent(text,"", predicate=lambda _: True)))



def output(txt):
    chat_query = txt

    prompt_template="""
        {priming}

        {question}

        {decorator}

        Your solution:
        """

    priming="""
            You are a friendly Agricultural Assistant. Your job is to help users find specific information related to agriculture. 
            You are capable of providing valuable information and assistance to farmers regarding various aspects of agriculture such as crop management, pest control, weather forecasting, market prices, and general farming queries, including basic queries and recommendations."""
    question = chat_query
    decorator="""- Make sure that you assist with agriculture related questions only and no other topics.
                 - Make sure that you answer to the point and elaborate only if the user asks to do so.
                 - If the user asks about your name, say AgriAssist. """
        
    prompt=prompt_template.format(priming=priming,
                            question=question,
                            decorator=decorator)
    completion=model.generate_content(prompt)
    return to_markdown(completion.text)

page_bg_img = '''
    <style>
    .stApp {
    background-image: url("https://images.pexels.com/photos/134879/pexels-photo-134879.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
    background-size: cover;
    }
    </style>
    ''' 
st.markdown(page_bg_img, unsafe_allow_html=True)
    

if "default" not in st.session_state:
    st.session_state["default"] = "output"
    
st.markdown("### Nature Bot")
with st.container(height=300, border=True):
    txt1 = st.text_area("Input",value=st.session_state["default"], height=300, on_change= callable,label_visibility="collapsed")
col1, col2 = st.columns([0.8,0.2])
with col1:
    txt = st.text_area("Input",value=None, height=30, placeholder="Ask your questions here",label_visibility="collapsed")
with col2:
    with st.container(height=10, border=False):
        pass
    Ask =st.button("Ask", type="primary", use_container_width=True)

if Ask:
    out = output(txt)
    st.session_state["default"] = out
    st.experimental_rerun()
