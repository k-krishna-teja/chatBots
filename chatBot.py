import os
import dotenv
import tkinter as tk
from tkinter import scrolledtext, Radiobutton, StringVar, Button
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

dotenv.load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL") # gemini-1.5-flash
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # A3zaSyA2ljk9PrtRZ-MJswTLFWdbsl5G2O0M7Eo

llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.7)

# Define templates for each chatbot
TEMPLATES = {
    "Educational": """
    You are an Educational Assistant trained to help students with their studies. You will:
    1. Explain concepts in various subjects
    2. Provide practice problems and solutions
    3. Answer questions related to the subject matter

    IMPORTANT: Always provide clear and accurate explanations.

    {input}
    """,
    "Language Learning": """
    You are a Language Learning Bot designed to help users learn a new language. You will:
    1. Engage in conversational practice
    2. Provide vocabulary exercises
    3. Explain grammar rules and concepts
    4. Answer questions about the language

    {input}
    """,
    "Entertainment": """
    You are an Entertainment Assistant trained to suggest movies, books, music, and games. You will:
    1. Provide recommendations based on user preferences
    2. Offer summaries and reviews
    3. Answer questions related to entertainment

    IMPORTANT: Always consider the user's preferences and interests.

    {input}
    """,
    "Medical": """
    You are an AI Medical Assistant trained to provide accurate medical information and guidance. You will:
    1. Answer medical questions with scientific accuracy
    2. Provide general health information and wellness advice
    3. Help interpret common medical terminology
    4. Suggest when to seek professional medical care

    You are only allowed to answer questions about the medical field.

    IMPORTANT: I am an AI assistant and cannot diagnose conditions or replace professional medical advice. For any serious medical concerns, please consult a qualified healthcare provider.

    {input}
    """
}

# Function to update the selected chatbot template
def update_template():
    global chain
    selected_template = chatbot_var.get()
    prompt = PromptTemplate.from_template(TEMPLATES[selected_template])
    chain = prompt | llm

def get_response():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        response = chain.invoke({"input": user_input})
        output_text.insert(tk.END, "You: " + user_input + "\n")
        output_text.insert(tk.END, "Bot: " + response.content + "\n\n")
        input_text.delete("1.0", tk.END)

# Create the main window
root = tk.Tk()
root.title("Chatbot Selector")
root.configure(bg='#e0e0e0')  # Set background color

# Radio buttons for chatbot selection
chatbot_var = StringVar(value="Educational")
for chatbot in TEMPLATES.keys():
    Radiobutton(root, text=chatbot, variable=chatbot_var, value=chatbot, command=update_template,
                bg='#e0e0e0', fg='#333333', selectcolor='#b0c4de', font=('Arial', 12)).pack(anchor=tk.W)

# Button to continue to chatbot GUI
continue_button = Button(root, text="Continue", command=lambda: show_chatbot_gui(root), bg='#4682b4', fg='white', font=('Arial', 12, 'bold'))
continue_button.pack(pady=10)

def show_chatbot_gui(main_window):
    main_window.withdraw()  # Hide the main window

    # Create the chatbot window
    chatbot_window = tk.Toplevel(main_window)
    chatbot_window.title(f"{chatbot_var.get()} Chatbot")
    chatbot_window.configure(bg='#f0f0f0')  # Set background color

    global input_text, output_text

    # Create the input text box
    input_text = tk.Text(chatbot_window, height=3, width=50, bg='#fffacd', fg='#333333', font=('Arial', 12))
    input_text.pack(pady=10)

    # Create the send button
    send_button = tk.Button(chatbot_window, text="Send", command=get_response, bg='#4682b4', fg='white', font=('Arial', 12, 'bold'))
    send_button.pack(pady=5)

    # Create the output text area
    output_text = scrolledtext.ScrolledText(chatbot_window, height=20, width=50, bg='#fafad2', fg='#333333', font=('Arial', 12))
    output_text.pack(pady=10)

    # Initial update of the template
    update_template()

# Start the Tkinter main loop
root.mainloop()
