import streamlit as st
from groq import Groq
from tavily import TavilyClient

st.set_page_config(page_title="Karachi AI Market", layout="centered")
st.title("🚀 Salman Bhai's AI Agent")

with st.sidebar:
    st.header("🔑 API Settings")
    g_key = st.text_input("Groq API Key", type="password")
    t_key = st.text_input("Tavily API Key", type="password")

user_query = st.text_input("Kiska rate chahiye? (e.g. iPhone 15, Petrol)")

if st.button("Market Check Karo!"):
    if g_key and t_key:
        tavily = TavilyClient(api_key=t_key)
        search_result = tavily.search(query=f"{user_query} current price in Karachi 2026", max_results=3)
        client = Groq(api_key=g_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a Karachi Market Expert. Respond in Roman Urdu."},
                {"role": "user", "content": f"Data: {search_result['results']}\n\nQuery: {user_query}"}
            ]
        )
        st.success(response.choices[0].message.content)
    else:
        st.warning("Sidebar mein keys daal dein!")
