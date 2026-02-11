import streamlit as st
from groq import Groq
from tavily import TavilyClient

st.set_page_config(page_title="Karachi AI Market Expert", page_icon="💰")
st.title("📈 Salman's Pro Agent")

# Sidebar for Keys
with st.sidebar:
    st.header("🔑 API Settings")
    g_key = st.text_input("Groq API Key", type="password")
    t_key = st.text_input("Tavily API Key", type="password")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Kiska rate chahiye?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not g_key or not t_key:
        st.error("Pehle sidebar mein Keys dalein!")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Latest market rate check ho raha hai..."):
                try:
                    # 1. Search (Updated to get CURRENT rates)
                    tavily = TavilyClient(api_key=t_key)
                    search = tavily.search(query=f"current official price of {prompt} in Karachi today", max_results=5)
                    
                    # 2. AI Brain
                    client = Groq(api_key=g_key)
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are a Karachi market expert. Always give the LATEST price from the search data. Respond in Roman Urdu."},
                            *st.session_state.messages,
                            {"role": "user", "content": f"Live Data: {search['results']}"}
                        ]
                    )
                    full_response = response.choices[0].message.content
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"Oho! Error aa gaya: {e}")
