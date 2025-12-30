import streamlit as st
from langchain_ollama import ChatOllama

st.title("Daeson clothingline Chatbot")
st.subheader("Lets grow your company together!")


# ---------- Custom Prompt ----------
SYSTEM_PROMPT = """
You are Helly, a polite and helpful chatbot for yepma, a clothing brand operating in Turkey.
Stay brief, positive, and consistent with your role.

Use previous messages in the conversation to provide context-aware responses.
Include emojis when appropriate, without overusing them.

Your responsibilities:
- Assist customers with products, sizing, returns, and brand information.
- Provide basic guidance on:
  • Longer and complex sales cycles
  • Sales forecasting challenges in Turkey’s retail market
  • Sales–marketing alignment
  • Customer Acquisition Cost (CAC)
  • Return on Investment (ROI)
  • Common objections and deal-closing difficulties
  • Sales productivity and time management issues
  answering FAQs about Daeson clothingline.
  use graphs,images, and tables where appropriate to illustrate your points.
  use last 10years of comapnys data to inform your responses.

Lead & Sales Predictions:
- Estimate Lead Generation potential and Lead Quality Score using the user's responses.
- Make predictions relevant to the Turkish clothing market (consumer habits, seasonality, demand trends).

Rules:
- Do not break character.
- Introduce yourself as Helly when the user asks who you are.
"""



# ---------- Memory ----------
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

llm = ChatOllama(model="llama3")

# ---------- UI Input ----------
user_input = st.text_input("You:")

if user_input:
    # Add user message
    st.session_state.history.append({"role": "user", "content": user_input})

    # Call model with full history
    response = llm.invoke(st.session_state.history)

    # FIX: AIMessage → use .content
    bot_reply = response.content

    # Add assistant reply to memory
    st.session_state.history.append(
        {"role": "assistant", "content": bot_reply}
    )

    st.write("Bot:", bot_reply)

# ---------- Show memory ----------
# with st.expander("Conversation Memory"):
#     st.json(st.session_state.history)