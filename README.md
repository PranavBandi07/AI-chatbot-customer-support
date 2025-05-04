# GPT-4 and Rule-Based Chatbot

This project implements a chatbot with two modes: a powerful GPT-4 based chatbot (using the Cheapest GPT-4 Turbo API via RapidAPI) and a rule-based chatbot that serves as a fallback or handles specific customer support scenarios.

## Features

* **GPT-4 Chatbot:**
    * Powered by the Cheapest GPT-4 Turbo API on RapidAPI.
    * Capable of generating human-like text responses.
    * Handles general conversation and a wide range of queries.
* **Rule-Based Chatbot:**
    * Provides pre-defined responses for specific customer support scenarios.
    * Handles common queries related to order status, returns, refunds, and other customer service issues.
    * Can be used as a fallback when the GPT-4 API is unavailable or for specific, simple interactions.
* **Chat Session History:**
    * Maintains a history of the conversation, including user messages and bot responses.
    * Saves the chat history to a JSON file (`chat_history.json`).
    * Option to load chat history from a file.
* **Chatbot Factory:**
    * Uses a factory pattern to create instances of either the GPT-4 chatbot or the rule-based chatbot.
    * Allows easy switching between chatbot types.

## Requirements

* Python 3.x
* `requests` library (`pip install requests`)
* A RapidAPI account and API key for the "Cheapest GPT-4 Turbo, GPT-4 Vision, ChatGPT Open AI..." API.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd <your_repository_directory>
    ```
2.  **Install the required Python library:**

    ```bash
    pip install requests
    ```
3.  **Obtain a RapidAPI key:**

    * Go to the [Cheapest GPT-4 Turbo, GPT-4 Vision, ChatGPT Open AI...](https://rapidapi.com/Hub-Team/api/cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai) API on RapidAPI.
    * Subscribe to the API and obtain your API key.
4.  **Set the RapidAPI key:**

    * Open the `main.py` file.
    * Replace `"YOUR_RAPIDAPI_KEY"` in the `if __name__ == "__main__":` block with your actual RapidAPI key.

## Usage

To use the chatbot:

1.  Run the `main.py` script:

    ```bash
    python main.py
    ```
2.  Interact with the chatbot in the terminal.
3.  Type `exit` to end the session.

**Important Notes for Coursework Defense:**

* The completed coursework (all files) must be submitted before or at the time of your presentation.
* The coursework report must be provided in Markdown format (`.md`) and should not exceed 7 pages.
* Your presentation should summarize your coursework clearly and concisely.
* Each presentation will be strictly limited to 5 minutes.
* The presentation must be supported by no more than 5 slides.
* Presentations will be delivered in front of the full lab audience.

## Switching between Chatbot Modes

The `run_chat` function defaults to using the GPT-4 chatbot. To use the rule-based chatbot, change the `chatbot_type` argument in the `if __name__ == "__main__":` block:

```python
if __name__ == "__main__":
    rapidapi_key = "YOUR_RAPIDAPI_KEY"  # Replace with your actual API key

    # To use the GPT-4 chatbot (default):
    run_chat(chatbot_type="gpt4", rapidapi_key=rapidapi_key)

    # To use the rule-based chatbot:
    # run_chat(chatbot_type="customer_support")
Important: API Key SecurityDo not hardcode your RapidAPI key directly in the script if you plan to share your code publicly.For better security, use environment variables or a configuration file to store your API key. For example, you could set an environment variable named RAPIDAPI_KEY and then retrieve it in your Python code.Code Structuremain.py: Contains the main application code, including:Abstract Chatbot class.GPT4Chatbot class for interacting with the GPT-4 API.CustomerSupportChatbot class for rule-based responses.ChatbotFactory for creating chatbot instances.ChatSession class for managing chat history.run_chat function to run the chat loop.chat_history.json: (Created after a chat session) Stores the conversation history in JSON format.Class DetailsChatbot (ABC): An abstract base class that defines the respond method.GPT4Chatbot: Implements the Chatbot interface to interact with the GPT-4 API.Uses the requests library to send POST requests to the API.Handles API authentication using the provided RapidAPI key.Parses the JSON response from the API to extract the chatbot's reply.CustomerSupportChatbot: Implements the Chatbot interface with a set of predefined rules for customer support interactions.ChatbotFactory: A factory class that creates instances of either GPT4Chatbot or CustomerSupportChatbot based on the specified type.ChatSession: A singleton class that manages the chat history.Stores messages and responses.Provides methods to save and load the history to/from a JSON file.Error HandlingThe code includes error handling for API requests:Handles requests.exceptions.RequestException to catch network errors or HTTP errors during API calls.Prints an error message to the console if the API returns an unexpected response.Future ImprovementsImplement more sophisticated
