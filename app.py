#!/usr/bin/env python3
"""
BouncingClippy Web App - A web-based chat interface with bouncing Clippy powered by Azure AI Foundry

SECURITY NOTE: This is a demo/educational application. Error messages are intentionally
exposed to help users understand and debug issues. For production deployments, error messages
should be sanitized to avoid exposing sensitive infrastructure details, stack traces, or
internal implementation information.
"""

import asyncio
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory

load_dotenv()

app = Flask(__name__)

# System message for Clippy's personality
CLIPPY_SYSTEM_MESSAGE = (
    "You are Clippy, the iconic Microsoft Office assistant! "
    "You're helpful, friendly, and enthusiastic. "
    "You love to assist users with their questions and always try to be encouraging. "
    "Keep your responses concise and helpful."
)

# Store chat sessions (in production, use Redis or a database with session expiration)
chat_sessions = {}


class BouncingClippy:
    """A chat application that uses Azure AI Foundry with Semantic Kernel for conversational AI."""
    
    def __init__(self):
        """Initialize the BouncingClippy chat app with Azure AI Foundry credentials."""
        self.endpoint = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT")
        self.api_key = os.environ.get("AZURE_AI_FOUNDRY_API_KEY")
        self.deployment_name = os.environ.get("AZURE_AI_FOUNDRY_MODEL", "gpt-4o")
        
        if not self.endpoint or not self.api_key:
            raise ValueError(
                "Missing required environment variables: "
                "AZURE_AI_FOUNDRY_ENDPOINT and AZURE_AI_FOUNDRY_API_KEY must be set"
            )
        
        # Initialize the Azure Chat Completion service with Semantic Kernel
        self.chat_service = AzureChatCompletion(
            endpoint=self.endpoint,
            api_key=self.api_key,
            deployment_name=self.deployment_name
        )
        
        # Create settings for chat completion
        self.settings = AzureChatPromptExecutionSettings()
        
        # Conversation history using Semantic Kernel's ChatHistory
        self.chat_history = ChatHistory()
        
        # Add a system message to set the personality
        self.chat_history.add_system_message(CLIPPY_SYSTEM_MESSAGE)
    
    async def send_message_async(self, user_prompt: str) -> str:
        """
        Send a user prompt to Azure AI Foundry and get a response asynchronously.
        
        Args:
            user_prompt: The user's message/prompt
            
        Returns:
            The AI's response as a string
        """
        # Add user message to conversation history
        self.chat_history.add_user_message(user_prompt)
        
        try:
            # Send to Azure AI Foundry via Semantic Kernel
            response = await self.chat_service.get_chat_message_content(
                chat_history=self.chat_history,
                settings=self.settings
            )
            
            # Extract the assistant's response
            assistant_message = str(response)
            
            # Add assistant response to conversation history
            self.chat_history.add_assistant_message(assistant_message)
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error communicating with Azure AI Foundry: {str(e)}"
            return error_msg
    
    def clear_history(self):
        """Clear the conversation history."""
        self.chat_history.clear()
        # Re-add system message
        self.chat_history.add_system_message(CLIPPY_SYSTEM_MESSAGE)


@app.route('/')
def index():
    """Serve the main page with bouncing Clippy and chat interface."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create chat session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = BouncingClippy()
        
        clippy = chat_sessions[session_id]
        
        # Get response from Azure AI (using asyncio.run for simplicity in this demo)
        # In production, consider using Flask's async support or an async web framework
        response = asyncio.run(clippy.send_message_async(user_message))
        
        return jsonify({
            'response': response,
            'session_id': session_id
        })
        
    except ValueError as e:
        # Expose error details for demo purposes
        print(f"Configuration error: {e}")
        return jsonify({'error': f'Configuration error: {str(e)}'}), 500
    except Exception as e:
        # Expose error details for demo purposes
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/api/clear', methods=['POST'])
def clear():
    """Clear the chat history for a session."""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        if session_id in chat_sessions:
            chat_sessions[session_id].clear_history()
        
        return jsonify({'success': True})
        
    except Exception as e:
        # Expose error details for demo purposes
        print(f"Error in clear endpoint: {e}")
        return jsonify({'error': f'An error occurred while clearing the chat: {str(e)}'}), 500


if __name__ == '__main__':
    # Check for required environment variables
    if not os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT") or not os.environ.get("AZURE_AI_FOUNDRY_API_KEY"):
        print("❌ Configuration Error:")
        print("Missing required environment variables:")
        print("  - AZURE_AI_FOUNDRY_ENDPOINT")
        print("  - AZURE_AI_FOUNDRY_API_KEY")
        print("\nPlease set these in your .env file or environment.")
        exit(1)
    
    print("🎉 Starting BouncingClippy Web App...")
    print("🌐 Open your browser to: http://localhost:5000")
    
    # Only enable debug mode if explicitly set in environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
