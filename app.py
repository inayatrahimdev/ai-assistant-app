import streamlit as st
from openai import AzureOpenAI

# === Page Setup ===
st.set_page_config(page_title="AI Assistant", layout="wide")
st.title("🔮 Azure OpenAI - Long Context Chat Assistant")

# === Azure Configuration ===
AZURE_OPENAI_KEY = "your-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_DEPLOYMENT_NAME = "o4-mini"  # Make sure this matches your Azure deployment
API_VERSION = "2025-01-01-preview"

# === AzureOpenAI Client ===
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version=API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

# === Session State for Chat History ===
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a highly intelligent assistant. "
                "Answer with deep, long, structured insights, suitable for research and forecasting."
            )
        }
    ]

# === User Input ===
user_input = st.text_area("🗣 Ask anything (long questions welcome):", height=150)

if st.button("🚀 Get Answer") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking... Generating long response..."):
        try:
            # Generate completion
            response = client.chat.completions.create(
                model=AZURE_DEPLOYMENT_NAME,
                messages=st.session_state.messages,
                max_completion_tokens=1024,  # ✅ Azure specific
                # temperature=1.0  # Optional — only include if supported by your deployment
            )

            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.markdown("### 🤖 Assistant's Response:")
            st.write(reply)

        except Exception as e:
            st.error(f"❌ Error: {e}")
