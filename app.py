

import streamlit as st
import requests
from groq import Groq
from bs4 import BeautifulSoup

client = Groq(
    api_key = st.secrets["GROQ_API_KEY"],
    )

st.set_page_config(page_title="The Analyser")
st.title("AI Market Intelligence Agent")
st.markdown("***Enter a company URL to analyze their current primary product focus.***")
st.divider()   

user_input = st.chat_input(placeholder="Eg: https://www.apple.com")

def Engine(data):

    # This is the prompt we send to the AI
    user_prompt = f"Based on this actual website text {data}, what is the main product they are pushing right now?"

    # The AI processing part
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
        {
            "role": "user",
            "content": user_prompt,
        }
    ],
    ) 
    return(completion.choices[0].message.content)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

if user_input:
    if not user_input.startswith("http"):
        st.error("Please enter valid URL")
    else:              
        r=requests.get(user_input, headers=headers, timeout=10)

        with st.spinner("Analising Website... Fetching Result..."):
            try:
              if r.status_code!=200:  
                st.error(f"Could not access website. ERROR CODE: " + {r.status_code})
              else:
                soup = BeautifulSoup(r.text, "html.parser")
                clean_text = soup.get_text()
                result = Engine(clean_text[:3000])
                st.success("Analysis Completed Successfully")
                st.subheader("Main Product Focus: ")
                st.info(result)
            
            except:
                st.error("An unexpected error occurred...")