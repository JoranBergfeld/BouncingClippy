#!/usr/bin/env python3
"""
BouncingClippy - A basic chat app powered by Azure AI Foundry with Semantic Kernel
"""

import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory

load_dotenv() 


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
        
    def add_system_message(self, content: str):
        """Add a system message to the conversation history."""
        self.chat_history.add_system_message(content)
    
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
            print(f"\n❌ {error_msg}")
            return error_msg
    
    def send_message(self, user_prompt: str) -> str:
        """
        Synchronous wrapper for send_message_async.
        
        Args:
            user_prompt: The user's message/prompt
            
        Returns:
            The AI's response as a string
        """
        return asyncio.run(self.send_message_async(user_prompt))
    
    def clear_history(self):
        """Clear the conversation history."""
        self.chat_history.clear()


def main():
    """Main function to run the BouncingClippy chat app."""
    print("=" * 60)
    print("🎉 Welcome to BouncingClippy! 🎉")
    print("=" * 60)
    print("A friendly chat app powered by Azure AI Foundry")
    print("\nCommands:")
    print("  - Type your message and press Enter to chat")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'quit' or 'exit' to end the chat")
    print("=" * 60)
    print()
    
    try:
        # Initialize the chat app
        clippy = BouncingClippy()
        
        # Add a system message to set the personality
        clippy.add_system_message(
            "You are BouncingClippy, a helpful and enthusiastic AI assistant. "
            "You're friendly, creative, and always eager to help users with their questions."
        )
        
        # Main chat loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                if user_input.lower() in ['quit', 'exit']:
                    print("\nThanks for chatting with BouncingClippy! Goodbye! 👋")
                    break
                
                if user_input.lower() == 'clear':
                    clippy.clear_history()
                    clippy.add_system_message(
                        "You are BouncingClippy, a helpful and enthusiastic AI assistant. "
                        "You're friendly, creative, and always eager to help users with their questions."
                    )
                    print("\n🔄 Conversation history cleared!\n")
                    continue
                
                # Send message and get response
                print("\nBouncingClippy: ", end="", flush=True)
                response = clippy.send_message(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\nChat interrupted. Goodbye! 👋")
                break
            except EOFError:
                print("\n\nEnd of input. Goodbye! 👋")
                break
                
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure you have set the required environment variables:")
        print("  - AZURE_AI_FOUNDRY_ENDPOINT")
        print("  - AZURE_AI_FOUNDRY_API_KEY")
        print("  - AZURE_AI_FOUNDRY_MODEL (optional, defaults to 'gpt-4o')")
        return 1
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
