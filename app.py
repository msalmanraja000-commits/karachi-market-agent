import streamlit as st
from groq import Groq
from tavily import TavilyClient

# Page Setup
st.set_page_config(page_title="Karachi AI Market Expert", page_icon="💰")
st.title("📈 Salman's Pro Market Agent")

# 🔐 Load Keys from Streamlit Secrets
# (Ab aapko sidebar mein kuch daalne ki zaroorat nahi!)
try:
    g_key = st.secrets["GROQ_API_KEY"]
    t_key = st.secrets["TAVILY_API_KEY"]
except Exception:
    st.error("Secrets setup nahi hain! Check your Streamlit Dashboard.")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Kiska rate chahiye? (e.g. Gold, iPhone, Petrol)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Market check ho rahi hai..."):
            try:
                # 1. Search
                tavily = TavilyClient(api_key=t_key)
                search = tavily.search(query=f"current official price of {prompt} in Karachi today", max_results=5)
                
                # 2. AI Response
                client = Groq(api_key=g_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a Karachi market expert. Use the search data. Speak Roman Urdu."},
                        *st.session_state.messages,
                        {"role": "user", "content": f"Live Data: {search['results']}"}
                    ]
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Masla aya: {e}")
