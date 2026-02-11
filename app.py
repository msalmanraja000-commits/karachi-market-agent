import streamlit as st from groq import Groq from tavily import TavilyClient

st.set_page_config(page_title="Karachi AI Market", layout="centered") st.title("🚀 Salman's AI Agent") st.subheader("Live Market Rates & Flipping Advice")

with st.sidebar: st.header("🔑 API Settings") g_key = st.text_input("Groq API Key", type="password") t_key = st.text_input("Tavily API Key", type="password")

user_query = st.text_input("Kiska rate chahiye? (e.g. iPhone 15, Petrol)")

if st.button("Market Check Karo!"): if not g_key or not t_key: st.error("Jigar, Sidebar mein dono API Keys toh daalo!") else: with st.spinner("Jasoosi jaari hai..."): try: tavily = TavilyClient(api_key=t_key) search_result = tavily.search(query=f"current market price of {user_query} in Karachi 2026", max_results=3) context = search_result['results']
