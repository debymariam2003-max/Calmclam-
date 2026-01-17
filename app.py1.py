import os
import streamlit as st
from huggingface_hub import InferenceClient

#Get token safely
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    st.error("HF_TOKEN not found. please set it as an environment variable or in secrets.toml")
    st.stop()

#Create Hugging Face client
client =InferenceClient(model = "meta-llama/Llama-3.1-8B-Instruct:novita", token=HF_TOKEN) 
   
#Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history =[]
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []
if "mood" not in  st.session_state:
    st.session_state.mood = "🙂 Normal"

# Sidebar: Emoji Mood Tracker
st.sidebar.header("✍️ Mood Tracker")
mood = st.sidebar.radio("How are you feeling today?" , ["🙂Normal", "😔Sadness", "😡Anger", "😁Joy", "😟Fear", "🤢Disgust", "🥱Ennui", "😩Anxiety", "🙄Envy", "🫣Embarassment"])
st.session_state.mood = mood
st.sidebar.write(f"selected mood: {mood}")

# Tabs for Chat, Journaling, Gratitude Jar and Moments
tab1, tab2, tab3, tab4 = st.tabs(["💬Chat", "📒Journaling", "🫙Gratitude Jar", "✨Moments"])

#LlaMa response function with follow-up
def get_wellness_response(user_message, mood):
    system_prompt = (
       f"You are a compassionate peace boosting chatbot for students. "
       f"The students is currently feeling {mood}. "
       "Detect emotional tone and respond with empathy, motivation, peace tips and relaxation tips. "
       "After your response, ask a gentle follow-up question to encourage reflection or complements")

    full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{user_message}\n<|assistant|>"
    response = client.text_generation(full_prompt, max_new_tokens=300, temperature=0.7)
    return response.strip()

# 💬Chat Tab
with tab1:
    st.title ("Calmness Booster Chatbot for students")
    st.markdown("Type how you are feeling. I'm here to support you with empathy and encourage you")

    user_input = st.text_area ("What's on your mind?", placeholder="e.g., 'I feel anxious and restless.'")

    if st.button("Send", key="chat_send"):
        if user_input:
            with st.spinner("Empathetically thinking.."):
                bot_reaponse = get_wellness_response(user_input, st.session_state.mood)
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", bot_reaponse))

#Display chat history
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")

#📒 Journal Tab
with tab2:
    st.title("Personal Journal")
    st.markdown("This is your personal space. Write your thoughts and anxieties here wihtout feeling judged")

    journal_input = st.text_area("A Pause to Breathe and Reflect my Day", placeholder="Little lessons from today")

    if st.button("Save Entry", key="journal_save"):
        if journal_input:
            st.session_state.journal_entries.append(journal_input)
            st.success("Journal entry saved!")

    if st.session_state.journal_entries:
        st.markdown("### ✍️ Your Entries")
        for i, entry in enumerate(st.session_state.journal_entries,1):
            st.markdown(f"**Entry {i}:** {entry}")
#🫙Gratitude Jar   
with tab3:
    st.title("Thank you note")   
    st.markdown("What I am thankful for")   

    journal_input = st.text_area("I am thankful for..", placeholder= "I am thankful that I was able to help someone")  

#✨Moments
with tab4:
    st.title("Core Memories")  
    st.markdown("Today's memories, be it sad, happy, embarassment or a mix of all the emotions")  

    journal_input = st.text_area("Islands of Personality", placeholder= "special, defining experiences")

