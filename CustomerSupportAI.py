import json
from abc import ABC, abstractmethod
import unittest
import requests

class Chatbot(ABC):
    """Abstract base class for chatbots."""

    @abstractmethod
    def respond(self, message: str, context: str = None) -> str:
        pass

class GPT4Chatbot(Chatbot):
    """Chatbot powered by the Cheapest GPT-4 Turbo API via RapidAPI."""

    def __init__(self, rapidapi_key):
        self.rapidapi_key = rapidapi_key
        self.api_url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"
        self.headers = {
            "content-type": "application/json",
            "X-RapidAPI-Host": "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com",
            "X-RapidAPI-Key": self.rapidapi_key
        }
        self.conversation_history = []
        self.model_name = "gpt-4o"  
        self.max_tokens = 1000
        self.temperature = 0.7

    def respond(self, message: str, context: str = None) -> str:
        self.conversation_history.append({"role": "user", "content": message})
        payload = {
            "messages": self.conversation_history,
            "model": self.model_name,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()

            
            if data and "choices" in data and len(data["choices"]) > 0 and "message" in data["choices"][0]:
                bot_response = data["choices"][0]["message"]["content"]
                self.conversation_history.append({"role": "assistant", "content": bot_response})
                return bot_response
            else:
                print(f"Unexpected GPT-4 API response: {data}")
                return "Sorry, I encountered an issue with the AI."

        except requests.exceptions.RequestException as e:
            print(f"Error calling GPT-4 API: {e}")
            return "Sorry, there was a problem communicating with the AI."

class CustomerSupportChatbot(Chatbot):
    """Concrete chatbot for customer support (rule-based fallback)."""
    def respond(self, message: str, context: str = None) -> str:
        message = message.lower()
        if context == "return_process":
            if "yes" in message:
                return "Please specify the item you'd like to return, and I can guide you through the return process."
            elif "no" in message:
                return "Okay! If you have any other questions or need further assistance, just let me know!"
        if "hello" in message or "hi" in message:
            return "Hello! How can I assist you with your order today?"
        elif "order status" in message:
            return "Please provide your order number to check the status."
        elif "return" in message or "refund" in message:
            return "You can return your item within 30 days for a full refund. Do you need assistance with the return process?"
        elif "how to return an item" in message:
            return "To return an item, please package it securely, include the invoice, and send it back to us using the provided label."
        elif "help" in message:
            return "Sure! What specific issue are you facing? I'd be happy to assist with returns, refunds, or tracking."
        elif "track" in message:
            return "Please provide your tracking number, and I can help you track your order."
        elif "thank you" in message:
            return "You're welcome! If you have any more questions, feel free to ask."
        elif "bye" in message or "goodbye" in message:
            return "Goodbye! Have a great day!"
        elif "item not received" in message:
            return "I'm sorry to hear that! Could you please provide your order number so I can check its status?"
        elif "missing item" in message:
            return "I apologize for the inconvenience. Please share your order number, and I'll look into it for you."
        elif "change order" in message:
            return "If you would like to change your order, please provide your order number and the changes you wish to make."
        elif "cancel order" in message:
            return "To cancel your order, please provide your order number, and I can assist you with the cancellation process."
        elif "payment issue" in message:
            return "If you're having a payment issue, please check your payment method. Would you like me to help you troubleshoot?"
        elif "account help" in message:
            return "For account-related issues, please describe the problem, and I'll do my best to assist you."
        elif "discount" in message or "coupon" in message:
            return "You can use special discount codes during checkout. If you have any specific code, please enter it!"
        else:
            return "I'm sorry, I didn't understand that. Can you please rephrase your question or ask about your order status, returns, or general inquiries?"

class ChatbotFactory:
    """Factory Method to create chatbot instances."""
    @staticmethod
    def create_chatbot(type: str, rapidapi_key: str = None) -> Chatbot:
        if type == "customer_support":
            return CustomerSupportChatbot()
        elif type == "gpt4":
            if rapidapi_key:
                return GPT4Chatbot(rapidapi_key)
            else:
                raise ValueError("RapidAPI key is required for GPT4Chatbot!")
        else:
            raise ValueError("Unknown chatbot type!")

class ChatSession:
    """Singleton class to manage chat session history."""
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatSession, cls).__new__(cls)
            cls._instance._history = []
        return cls._instance
    def add_to_history(self, message: str, response: str):
        self._history.append({"message": message, "response": response})
    def save_history(self, filename: str):
        with open(filename, 'w') as file:
            json.dump(self._history, file, indent=4)
    def load_history(self, filename: str):
        try:
            with open(filename, 'r') as file:
                self._history = json.load(file)
        except FileNotFoundError:
            print("No history found.")
    @property
    def history(self):
        return self._history

class TestChatSession(unittest.TestCase):
    """Unit tests for ChatSession."""
    def setUp(self):
        self.session = ChatSession()
        self.session._history = []  
    def test_add_to_history(self):
        self.session.add_to_history("Hello", "Hello! How can I assist you with your order today?")
        self.assertEqual(len(self.session.history), 1)
    def test_save_load_history(self):
        self.session.add_to_history("Hello", "Hello! How can I assist you with your order today?")
        self.session.save_history("test_history.json")
        new_session = ChatSession()
        new_session.load_history("test_history.json")
        self.assertEqual(len(new_session.history), 1)

def run_chat(chatbot_type="customer_support", rapidapi_key=None):
    """Main chat loop."""
    factory = ChatbotFactory()
    try:
        chatbot = factory.create_chatbot(chatbot_type, rapidapi_key)
        print(f"API URL being used: {chatbot.api_url}")
        print(f"Headers being sent: {chatbot.headers}")
    except ValueError as e:
        print(f"Error creating chatbot: {e}")
        return

    chat_session = ChatSession()
    context = None

    print(f"Welcome to the Chatbot ({chatbot_type.replace('_', ' ').title()})! Type 'exit' to end the chat.")

    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            break

        response = chatbot.respond(user_message, context)
        chat_session.add_to_history(user_message, response)
        print(f"Bot: {response}")

        if isinstance(chatbot, CustomerSupportChatbot):
            if "need assistance with the return process" in response:
                context = "return_process"
            else:
                context = None

    chat_session.save_history("chat_history.json")

if __name__ == "__main__":
    
    rapidapi_key = "520e9f0b0dmshb0f5eebfa5a14cbp1ae023jsnb163083f4c52"
    run_chat(chatbot_type="gpt4", rapidapi_key=rapidapi_key)

    
    