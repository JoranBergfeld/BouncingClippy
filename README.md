# BouncingClippy 🎉

A demonstration chat application showcasing **Azure AI integration** using **Semantic Kernel** and **Azure AI Foundry**. BouncingClippy provides an interactive command-line interface for conversational AI, highlighting key integration points with Azure's AI services.

## What is BouncingClippy?

BouncingClippy is a sample application designed to demonstrate how to integrate Azure AI services into Python applications. It showcases:

- **Azure AI Foundry Integration**: Connecting to Azure-hosted AI models
- **Semantic Kernel Framework**: Microsoft's open-source SDK for AI orchestration
- **Chat Completion API**: Building conversational AI experiences
- **Conversation History Management**: Maintaining context across multiple turns
- **Async/Await Patterns**: Modern Python async programming with AI services

This app serves as a reference implementation for developers looking to understand Azure AI integration patterns and build their own AI-powered applications.

## Key Integration Points

### 🔌 Azure AI Foundry Connection
The app demonstrates how to connect to Azure AI Foundry services using:
- Endpoint URL configuration
- API key authentication
- Model deployment selection

### 🧠 Semantic Kernel Framework
Built on Microsoft's Semantic Kernel, showcasing:
- `AzureChatCompletion` service integration
- `ChatHistory` for conversation management
- `AzureChatPromptExecutionSettings` for request configuration
- Async chat completion patterns

### 💬 Conversational AI Patterns
Implements common patterns for chat applications:
- System message prompts for personality
- Multi-turn conversation context
- Error handling and retry logic
- Clean conversation reset functionality

## Features

- 💬 **Interactive CLI**: Real-time chat interface with streaming responses
- 🔄 **Context Awareness**: Multi-turn conversations with full history
- ⚙️ **Configurable Models**: Easy switching between different Azure AI models
- 🧹 **Session Management**: Clear conversation history on demand
- 🎨 **Simple Setup**: Environment-based configuration with `.env` support

## Prerequisites

- **Python 3.10 or higher**
- **Azure Subscription** with access to Azure AI Foundry
- **Azure AI Foundry Resources**:
  - A deployed AI model (e.g., GPT-4o, GPT-4, GPT-3.5-Turbo)
  - Project endpoint URL
  - API key for authentication

## Installation

### 1. Clone or Download this Repository

```bash
git clone <repository-url>
cd basic-foundry-chat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `semantic-kernel>=1.37.0` - Microsoft's AI orchestration framework
- `python-dotenv>=1.0.0` - Environment variable management

### 3. Configure Azure Credentials

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` and add your Azure AI Foundry credentials:

```env
AZURE_AI_FOUNDRY_ENDPOINT=https://your-resource.services.ai.azure.com
AZURE_AI_FOUNDRY_API_KEY=your-api-key-here
AZURE_AI_FOUNDRY_MODEL=gpt-4o
```

**Where to find these values:**
1. Go to [Azure AI Foundry Portal](https://ai.azure.com/)
2. Select your project
3. Navigate to **Deployments** to see your deployed models
4. Go to **Project settings** to find your endpoint and API keys

## Running the Application

### Standard Execution

```bash
python bouncing_clippy.py
```

### Alternative: Using Environment Variables Directly

**PowerShell:**
```powershell
$env:AZURE_AI_FOUNDRY_ENDPOINT="https://your-resource.services.ai.azure.com"
$env:AZURE_AI_FOUNDRY_API_KEY="your-api-key-here"
$env:AZURE_AI_FOUNDRY_MODEL="gpt-4o"
python bouncing_clippy.py
```

**Bash/Linux:**
```bash
export AZURE_AI_FOUNDRY_ENDPOINT="https://your-resource.services.ai.azure.com"
export AZURE_AI_FOUNDRY_API_KEY="your-api-key-here"
export AZURE_AI_FOUNDRY_MODEL="gpt-4o"
python bouncing_clippy.py
```

## Usage

### Available Commands

Once running, BouncingClippy accepts the following commands:

| Command | Description |
|---------|-------------|
| `<your message>` | Chat with the AI - just type and press Enter |
| `clear` | Clear conversation history and start fresh |
| `quit` or `exit` | Exit the application |

### Example Session

```
============================================================
🎉 Welcome to BouncingClippy! 🎉
============================================================
A friendly chat app powered by Azure AI Foundry

Commands:
  - Type your message and press Enter to chat
  - Type 'clear' to clear conversation history
  - Type 'quit' or 'exit' to end the chat
============================================================

You: Hello! Can you explain what you are?

BouncingClippy: Hi there! I'm BouncingClippy, a helpful AI assistant powered 
by Azure AI Foundry. I'm here to demonstrate how Azure's AI services can be 
integrated into applications using Semantic Kernel...

You: What can you help me with?

BouncingClippy: I can assist with a variety of tasks...

You: clear

🔄 Conversation history cleared!

You: quit

Thanks for chatting with BouncingClippy! Goodbye! 👋
```

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AZURE_AI_FOUNDRY_ENDPOINT` | ✅ Yes | - | Your Azure AI Foundry endpoint URL (e.g., `https://*.services.ai.azure.com`) |
| `AZURE_AI_FOUNDRY_API_KEY` | ✅ Yes | - | Your Azure AI Foundry API key |
| `AZURE_AI_FOUNDRY_MODEL` | ⚠️ Optional | `gpt-4o` | The deployment name of your model |

### Common Model Deployment Names

- `gpt-4o` - GPT-4 Optimized (recommended)
- `gpt-4` - GPT-4 standard
- `gpt-35-turbo` - GPT-3.5 Turbo
- `gpt-4o-mini` - GPT-4 Mini (cost-effective)

**Note:** Use the exact deployment name from your Azure AI Foundry project.

## Architecture Overview

### Technology Stack

```
┌─────────────────────────────────────┐
│     BouncingClippy (Python CLI)     │
├─────────────────────────────────────┤
│      Semantic Kernel (1.37.x)       │
├─────────────────────────────────────┤
│    AzureChatCompletion Service      │
├─────────────────────────────────────┤
│      Azure AI Foundry Endpoint      │
├─────────────────────────────────────┤
│    Azure OpenAI / AI Models         │
└─────────────────────────────────────┘
```

### Code Structure

```
bouncing_clippy.py          # Main application
├── BouncingClippy class    # Chat orchestration
│   ├── __init__()          # Azure service setup
│   ├── send_message()      # Message handling
│   └── clear_history()     # Session management
└── main()                  # CLI interface

requirements.txt            # Python dependencies
.env                       # Azure credentials (gitignored)
.env.example              # Configuration template
README.md                 # This file
```

## Troubleshooting

### Import Errors

**Error:** `Import "semantic_kernel.connectors.ai.open_ai" could not be resolved`

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Authentication Errors

**Error:** `Missing required environment variables`

**Solution:** 
1. Ensure `.env` file exists with correct values
2. Verify no extra spaces in environment variable values
3. Check that the file is named `.env` (not `.env.txt`)

### Connection Errors

**Error:** `Error communicating with Azure AI Foundry: 404 Resource not found`

**Solutions:**
- Verify endpoint URL format: `https://*.services.ai.azure.com` (no `/inference` suffix)
- Confirm model deployment name matches exactly (case-sensitive)
- Check API key is valid and not expired
- Ensure your Azure subscription has the model deployed

**Error:** `401 Unauthorized`

**Solution:** Verify your API key is correct and has proper permissions

### Model Errors

**Error:** `The API deployment for this resource does not exist`

**Solution:**
1. Go to Azure AI Foundry Portal → Your Project → Deployments
2. Copy the exact deployment name
3. Update `AZURE_AI_FOUNDRY_MODEL` in `.env`

## Learning Resources

### Azure AI Foundry
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Getting Started Guide](https://learn.microsoft.com/azure/ai-studio/how-to/develop/sdk-overview)
- [Deploy Models Tutorial](https://learn.microsoft.com/azure/ai-studio/how-to/deploy-models)

### Semantic Kernel
- [Semantic Kernel Documentation](https://learn.microsoft.com/semantic-kernel/overview/)
- [Python Quick Start](https://learn.microsoft.com/semantic-kernel/get-started/quick-start-guide?pivots=programming-language-python)
- [Chat Completion Guide](https://learn.microsoft.com/semantic-kernel/concepts/ai-services/chat-completion/)

## Next Steps

Once you have BouncingClippy running, consider exploring:

1. **Add Plugins**: Extend with custom functions using Semantic Kernel plugins
2. **Streaming Responses**: Implement streaming for real-time token generation
3. **Multiple Agents**: Build multi-agent conversations
4. **Vector Search**: Integrate Azure AI Search for RAG patterns
5. **Web Interface**: Convert to a web app using Flask or FastAPI
6. **Function Calling**: Add tool use and function calling capabilities

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! This is a demonstration app meant to help developers learn Azure AI integration patterns. Feel free to:

- Submit issues for bugs or questions
- Create pull requests with improvements
- Share feedback on integration patterns
- Suggest new features or examples

## Support

For issues related to:
- **This app**: Open a GitHub issue
- **Azure AI Foundry**: Visit [Azure Support](https://azure.microsoft.com/support/)
- **Semantic Kernel**: Check [Semantic Kernel GitHub](https://github.com/microsoft/semantic-kernel)
