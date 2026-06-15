import pandas as pd
import random
import nltk
import tkinter as tk
from tkinter import scrolledtext
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Preprocess the text using NLTK
def preprocess_text(text):
    tokens = word_tokenize(text)  # Tokenize the input text
    tokens = [word.lower() for word in tokens]  # Lowercase the tokens
    stop_words = set(stopwords.words('english'))  # English stopwords
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]  # Remove stopwords and non-alphabetic tokens
    
    # Optionally, apply stemming
    ps = PorterStemmer()
    stemmed_tokens = [ps.stem(word) for word in filtered_tokens]  # Stemming
    
    return ' '.join(stemmed_tokens)

# Load the CSV data
class MentalHealthChatbot:
    def __init__(self, csv_file):
        self.data = pd.read_csv('chethan.csv')
        self.questions = self.data['Questions'].tolist()
        self.answers = self.data['Answers'].tolist()

    def get_response(self, user_input):
        preprocessed_input = preprocess_text(user_input)  # Preprocess the input
        
        # Match the preprocessed input with stored questions
        for question in self.questions:
            if preprocess_text(question) in preprocessed_input:
                return random.choice(self.answers)  # Return a random answer if match found
        return "I'm sorry, I don't understand. Can you ask something else?"

# Chat interface
class ChatInterface:
    def __init__(self, master, chatbot):
        self.master = master
        self.chatbot = chatbot
        master.title("Mental Health Chatbot")

        # Chat area to display conversation
        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', wrap=tk.WORD)
        self.chat_area.grid(row=0, column=0, columnspan=2)

        # Input field for the user
        self.user_input = tk.Entry(master, width=80)
        self.user_input.grid(row=1, column=0)

        # Send button to submit user input
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1)

    def send_message(self):
        user_text = self.user_input.get()
        if user_text.lower() == 'exit':
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, "Chatbot: Goodbye! Take care.\n")
            self.chat_area.config(state='disabled')
            return
        
        # Display user input in the chat area
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"You: {user_text}\n")
        
        # Get and display the chatbot's response
        response = self.chatbot.get_response(user_text)
        self.chat_area.insert(tk.END, f"Chatbot: {response}\n")
        
        # Clear the input field
        self.user_input.delete(0, tk.END)
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

# Main function to run the chatbot
def main():
    chatbot = MentalHealthChatbot('chethan.csv')  # Assuming 'ty.csv' contains your questions and answers
    
    root = tk.Tk()  # Create the Tkinter window
    chat_interface = ChatInterface(root, chatbot)  # Create the chat interface
    
    root.mainloop()  # Run the GUI loop

if __name__ == "__main__":
    main()
