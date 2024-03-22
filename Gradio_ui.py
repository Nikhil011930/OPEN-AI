# Import required libraries
import os
import requests
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Load the environment variables from the .env file
load_dotenv(find_dotenv())

# Configure the GenerativeAI API key
genai.configure(api_key = os.getenv("GEN_API_KEY"))

# Create a GenerativeAI model
model = genai.GenerativeModel()


# Define the handle_user_query function
def handle_user_query(msg, chatbot):
    """
    Handle the user's query by adding it to the chatbot and returning an empty string.

    Args:
        msg (str): The user's query.
        chatbot (list[list[str,str]]): The current state of the chatbot.

    Returns:
        str: An empty string.
    """
    print(msg, chatbot)
    chatbot += [[msg, None]]
    return '', chatbot

# Define the handle_gemini_response function
def generate_chatbot(chatbot: list[list[str,str]]) -> list[list[str, str]]:
    """
    Format the chatbot data into a list of dictionaries, with each dictionary representing a message in the chatbot.

    Args:
        chatbot (list[list[str,str]]): The current state of the chatbot.

    Returns:
        list[list[str, str]]: A list of dictionaries representing the chatbot data.
    """
    formatted_chatbot = []
    if len(chatbot) == 0:
        return formatted_chatbot
    for ch in chatbot:
        formatted_chatbot.append(
            {
                "role": "user" if ch[0] == "" else "assistant",
                "parts": ch[0]
            }
        )
        formatted_chatbot.append(
            {
                'role' : 'model',
                'parts' : ch[1]
            }
        )

# Define the handle_gemini_response function
def handle_gemini_response(chatbot):
    """
    Handle the response from the GenerativeAI model by adding it to the chatbot.

    Args:
        chatbot (list[list[str,str]]): The current state of the chatbot.

    Returns:
        list[list[str, str]]: The updated chatbot with the response from the GenerativeAI model.
    """
    query = chatbot[-1][0]
    formated_chatbot = generate_chatbot(chatbot[:-1])
    chat = model.start_chat(history = formated_chatbot)
    response = chat.send_message(query)
    chatbot[-1][1] = response.text
    
    return chatbot

# Define the demo block
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        label="Chat With Me",
        bubble_full_width=False 
    )
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    msg.submit(
        handle_user_query,
        [msg, chatbot],
        [msg, chatbot]
    ).then(
        handle_gemini_response,
        [chatbot],
        [chatbot]
    )

# Launch the demo
if __name__ == "__main__":
    demo.queue()
    demo.launch()