import streamlit as st

######## Setting the overall page configuration ########
st.set_page_config(
    layout='wide',
    page_title='AiTHLETES F1 Hub | F1 Pilot',
    page_icon="🏎️",
    initial_sidebar_state='collapsed'
)

######## Setting a new style for the page ########
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



"""
Chat Version 3
    ✅ Chat User and Assistant
    ✅ History (all messages)
    ✅ Animation when displaying the assistant message
"""

import random
import time
import streamlit as st

from chat_bot import F1ChatBot
from util import *
from prompt_list import prompts

# [i]                                                                                            #
# [i] Initialize FrontEnd App                                                                    #
# [i]                                                                                            #

def initialize() -> None:
    """
    Initialize the app
    """

    with st.expander("Bot Configuration"):
        st.selectbox(label="Prompt", options=["prompt1", "prompt2"])
        st.session_state.system_behavior = st.text_area(
            label="Prompt",
            value=prompts[0]["prompt"]
        )

    st.sidebar.title("🤖🏎️ F1 ChatBot")

    if "chatbot" not in st.session_state:
        st.session_state.chatbot = F1ChatBot(st.session_state.system_behavior)

    with st.sidebar:
        st.markdown(
            f"ChatBot in use: <font color='cyan'>{st.session_state.chatbot.__str__()}</font>", unsafe_allow_html=True
        )


# [i]                                                                                            #
# [i] Display History Message                                                                    #
# [i]                                                                                            #

def display_history_messages():
    # Display chat messages from history on app rerun
    for message in st.session_state.chatbot.memory:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# [i]                                                                                            #
# [i] Display User Message                                                                       #
# [i]                                                                                            #

def display_user_msg(message: str):
    """
    Display user message in chat message container
    """
    with st.chat_message("user", avatar="😎"):
        st.markdown(message)


# [i]                                                                                            #
# [i] Display User Message                                                                       #
# [i]                                                                                            #

def display_assistant_msg(message: str, animated=True):
    """
    Display assistant message
    """

    if animated:
        with st.chat_message("assistant", avatar="🏎️"):
            message_placeholder = st.empty()

            # Simulate stream of response with milliseconds delay
            full_response = ""
            for chunk in message.split():
                full_response += chunk + " "
                time.sleep(0.05)

                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
    else:
        with st.chat_message("assistant", avatar="🤖🏎️"):
            st.markdown(message)


# [*]                                                                                            #
# [*] MAIN                                                                                       #
# [*]                                                                                            #

if __name__ == "__main__":
    initialize()

    # [i] Display History #
    display_history_messages()

    if prompt := st.chat_input("Type your request..."):

        # [*] Request & Response #
        display_user_msg(message=prompt)
        assistant_response = st.session_state.chatbot.generate_response(
            message=prompt
        )
        display_assistant_msg(message=assistant_response)


    # [i] Sidebar #
    with st.sidebar:
        with st.expander("Information"):
            if local_settings.OPENAI_API_KEY:
                st.write(f"🔑 Key loaded...")

            st.text("💬 MEMORY")
            st.write(st.session_state.chatbot.memory)







####To Finish Off the Sidebar with Trademark
st.sidebar.markdown('''
---
Website developed for the \n Capstone Project Course
                    
                    © AiTHLETES  
''') 

st.sidebar.markdown("Social Media Links")


st.sidebar.markdown('<a href="https://twitter.com/AiTHLETS" target="_blank"><img src="https://img.freepik.com/vetores-gratis/novo-design-de-icone-x-do-logotipo-do-twitter-em-2023_1017-45418.jpg?size=338&ext=jpg&ga=GA1.1.1412446893.1704585600&semt=ais" height="30" width="30" style="border-radius: 50%;"></a >'
                    '&nbsp;&nbsp;&nbsp;'
                        '<a href="https://www.instagram.com/f1_aithletes/" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png" height="30" width="30" style="border-radius: 50%;"></a>', unsafe_allow_html=True)
                        