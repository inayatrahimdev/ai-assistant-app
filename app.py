import streamlit as st
from openai import AzureOpenAI

# --- Azure OpenAI Config ---
AZURE_OPENAI_KEY = st.secrets["AZURE_OPENAI_KEY"]
AZURE_OPENAI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"]
AZURE_DEPLOYMENT_NAME = st.secrets["AZURE_DEPLOYMENT_NAME"]
API_VERSION = "2025-01-01-preview"

# --- Azure Client Init ---
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version=API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

# --- Streamlit Page Setup ---
st.set_page_config(page_title="🔮 Azure OpenAI Chat Assistant", page_icon="🔮")
st.title("🔮 Azure OpenAI - Long Context Chat Assistant")
st.markdown("🗣 **Ask anything — long or short questions welcome!**")

# --- User Input ---
user_input = st.text_area("💬 Enter your message below:", height=150, placeholder="What is AI?")

# --- Handle Submit ---
if st.button("Ask AI"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a message before submitting.")
    else:
        with st.spinner("🤖 Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=AZURE_DEPLOYMENT_NAME,
                    messages=[
                        {"role": "system", "content": "You are a helpful, intelligent AI assistant."},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=1,  # ✅ FIXED: Only temperature=1 is supported in your Azure model
                    max_completion_tokens=1024,
                )
                assistant_reply = response.choices[0].message.content.strip()
                st.success("✅ Assistant's Response:")
                st.markdown(assistant_reply)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
