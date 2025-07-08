# Polli-Agent 🌸

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Pollinations](https://img.shields.io/badge/Powered%20by-Pollinations-ff6b9d)](https://pollinations.ai)
 ![Production Ready]( https://img.shields.io/badge/Status-Production%20Ready-green)

*Polli-Agent is a production-ready AI coding assistant powered by Pollinations AI models.*

**Polli-Agent** is an advanced LLM-based agent specifically designed for software engineering tasks, powered by [Pollinations AI](https://pollinations.ai). It provides a powerful CLI interface that understands natural language instructions and executes complex coding workflows using multiple Pollinations models including OpenAI, DeepSeek, Qwen, and Mistral.

**What Makes Polli-Agent Special:** Polli-Agent combines the power of multiple Pollinations AI models with a transparent, modular architecture. Unlike other agents, it offers **seamless multi-model switching**, **optional API key usage** (works with free tier), and **production-ready stability**. The Pollinations integration provides access to cutting-edge models like DeepSeek Reasoning, Qwen Coder, and Mistral, all through a unified interface.

**Project Status:** Polli-Agent is **production-ready** and actively maintained. Built on the solid foundation of Trae-Agent, it's specifically optimized for Pollinations AI models with full tool calling support, multi-model capabilities, and robust error handling.

## ✨ Features

- 🌸 **Pollinations AI Integration**: Native support for multiple Pollinations models
- 🔄 **Multi-Model Support**: OpenAI, DeepSeek Reasoning, Qwen Coder, Mistral, and more
- 🆓 **Optional API Key**: Works with free tier (no API key) or premium models (with API key)
- 🌊 **Lakeview**: Provides short and concise summarisation for agent steps
- 🛠️ **Rich Tool Ecosystem**: File editing, bash execution, sequential thinking, and more
- 🎯 **Interactive Mode**: Conversational interface for iterative development
- 📊 **Trajectory Recording**: Detailed logging of all agent actions for debugging and analysis
- ⚙️ **Flexible Configuration**: JSON-based configuration with environment variable support
- 🚀 **Easy Installation**: Simple uv-based installation

## 🚀 Quick Start

### Installation

We strongly recommend using [UV](https://docs.astral.sh/uv/) to setup the project.

```bash
git clone https://github.com/pollinations/polli-agent.git
cd polli-agent
uv sync
```

### Global Installation (Recommended)

To use `polli` command globally from anywhere:

#### Option 1: Quick Install Script
```bash
git clone https://github.com/pollinations/polli-agent.git
cd polli-agent
./install.sh
```

#### Option 2: Manual Install
```bash
git clone https://github.com/pollinations/polli-agent.git
cd polli-agent
pip install -e .
```

After installation, you can use `polli` from anywhere:
```bash
polli run "Create a Python script"
polli interactive
polli --help
```

### Development Setup

For development, use UV to set up the project:
```bash
git clone https://github.com/pollinations/polli-agent.git
cd polli-agent
uv sync
# Use: uv run polli [command]
```

### Setup API Keys

**Polli-Agent works with or without an API key!**

#### Option 1: Free Tier (No API Key Required)
Polli-Agent works out of the box with basic Pollinations models:
```bash
# No setup needed - just start using it!
polli run "Create a hello world Python script"
```

#### Option 2: Premium Models (API Key Required)
For access to premium models like DeepSeek, Qwen, and Mistral:

**Environment Variable (Recommended):**
```bash
export POLLINATIONS_API_KEY="your-pollinations-api-key"
```

**Or in Config File:**
```json
{
  "model_providers": {
    "pollinations": {
      "api_key": "your-pollinations-api-key"
    }
  }
}
```

### Basic Usage

```bash
# Run with default model (OpenAI GPT-4o Mini - free tier)
polli run "Create a hello world Python script"

# Use specific Pollinations models (just select the provider!)
polli run "Create a Python script" --provider openai
polli run "Debug complex code" --provider deepseek-reasoning
polli run "Write documentation" --provider qwen-coder
polli run "Refactor code" --provider mistral
polli run "Large project analysis" --provider openai-large
```

## 📖 Usage

### Command Line Interface

The main entry point is the `polli` command with several subcommands:

#### `polli run` - Execute a Task

```bash
# Basic task execution (uses default OpenAI model)
polli run "Create a Python script that calculates fibonacci numbers"

# With specific Pollinations models (pre-configured providers)
polli run "Fix the bug in main.py" --provider deepseek-reasoning
polli run "Optimize this code" --provider openai-large
polli run "Add documentation" --provider qwen-coder
polli run "Refactor code" --provider mistral
polli run "Fast coding task" --provider openai-fast
polli run "Advanced reasoning" --provider grok

# With custom working directory
polli run "Add unit tests for the utils module" --working-dir /path/to/project

# Save trajectory for debugging
polli run "Refactor the database module" --trajectory-file debug_session.json

# With API key for premium models
polli run "Complex analysis" --provider deepseek-reasoning --api-key "your-key"

# Force to generate patches
polli run "Update the API endpoints" --must-patch
```

#### `polli interactive` - Interactive Mode

```bash
# Start interactive session with default model
polli interactive

# With specific Pollinations models
polli interactive --provider deepseek-reasoning --max-steps 30
polli interactive --provider qwen-coder
polli interactive --provider grok
```

In interactive mode, you can:
- Type any task description to execute it
- Use `status` to see agent information
- Use `help` for available commands
- Use `clear` to clear the screen
- Use `exit` or `quit` to end the session

#### `trae show-config` - Configuration Status

```bash
polli show-config

# With custom config file
polli show-config --config-file my_config.json
```

### Configuration

Polli-Agent uses a JSON configuration file (`trae_config.json`) with **pre-configured providers** for each model:

```json
{
  "default_provider": "openai",
  "max_steps": 20,
  "enable_lakeview": true,
  "model_providers": {
    "openai": {
      "api_key": "",
      "model": "openai",
      "max_tokens": 4096,
      "temperature": 0.7,
      "top_p": 1,
      "max_retries": 10
    },
    "anthropic": {
      "api_key": "your_anthropic_api_key",
      "model": "claude-sonnet-4-20250514",
      "max_tokens": 4096,
      "temperature": 0.5,
      "top_p": 1,
      "top_k": 0,
      "max_retries": 10
    },
    "azure": {
      "api_key": "you_azure_api_key",
      "base_url": "your_azure_base_url",
      "api_version": "2024-03-01-preview",
      "model": "model_name",
      "max_tokens": 4096,
      "temperature": 0.5,
      "top_p": 1,
      "top_k": 0,
      "max_retries": 10
    },
    "openrouter": {
      "api_key": "your_openrouter_api_key",
      "model": "openai/gpt-4o",
      "max_tokens": 4096,
      "temperature": 0.5,
      "top_p": 1,
      "top_k": 0,
      "max_retries": 10
    },
    "doubao": {
      "api_key": "you_doubao_api_key",
      "model": "model_name",
      "base_url": "your_doubao_base_url",
      "max_tokens": 8192,
      "temperature": 0.5,
      "top_p": 1,
      "max_retries": 20
    }
  },
  "lakeview_config": {
    "model_provider": "anthropic",
    "model_name": "claude-sonnet-4-20250514"
  }
}
```

**Configuration Priority:**
1. Command-line arguments (highest)
2. Configuration file values
3. Environment variables
4. Default values (lowest)

```bash
# Use different Pollinations models for specific tasks (pre-configured providers)
polli run "Write a Python script" --provider openai
polli run "Debug complex code" --provider deepseek-reasoning
polli run "Generate documentation" --provider qwen-coder
polli run "Refactor legacy code" --provider mistral
polli run "Large codebase analysis" --provider openai-large
polli run "Fast development" --provider openai-fast
polli run "Advanced reasoning" --provider grok
polli run "Latest AI capabilities" --provider llama-scout
```

**Available Pre-Configured Providers:**
- `openai` - General purpose, works without API key (default)
- `deepseek-reasoning` - Excellent for complex problem solving
- `qwen-coder` - Specialized for coding tasks
- `mistral` - Fast and efficient for most tasks
- `openai-large` - Enhanced capabilities for complex projects
- `openai-fast` - Speed-optimized for quick tasks
- `grok` - Advanced reasoning capabilities
- `llama-scout` - Latest Llama 4 Scout model
- `deepseek` - DeepSeek V3 model
- `phi` - Microsoft Phi-4 with vision support

### Environment Variables

- `POLLINATIONS_API_KEY` - Pollinations API key (optional - works without for basic models)

**Note:** Unlike other agents, Polli-Agent works perfectly without any API key for basic models. Set `POLLINATIONS_API_KEY` only if you want access to premium models like DeepSeek, Qwen, and Mistral.

## 🛠️ Available Tools

Trae Agent comes with several built-in tools:

- **str_replace_based_edit_tool**: Create, edit, view, and manipulate files
  - `view` - Display file contents or directory listings
  - `create` - Create new files
  - `str_replace` - Replace text in files
  - `insert` - Insert text at specific lines

- **bash**: Execute shell commands and scripts
  - Run commands with persistent state
  - Handle long-running processes
  - Capture output and errors

- **sequential_thinking**: Structured problem-solving and analysis
  - Break down complex problems
  - Iterative thinking with revision capabilities
  - Hypothesis generation and verification

- **task_done**: Signal task completion
  - Mark tasks as successfully completed
  - Provide final results and summaries

## 📊 Trajectory Recording

Trae Agent automatically records detailed execution trajectories for debugging and analysis:

```bash
# Auto-generated trajectory file
polli run "Debug the authentication module"
# Saves to: trajectory_20250612_220546.json

# Custom trajectory file
polli run "Optimize the database queries" --trajectory-file optimization_debug.json
```

Trajectory files contain:
- **LLM Interactions**: All messages, responses, and tool calls
- **Agent Steps**: State transitions and decision points
- **Tool Usage**: Which tools were called and their results
- **Metadata**: Timestamps, token usage, and execution metrics

For more details, see [TRAJECTORY_RECORDING.md](TRAJECTORY_RECORDING.md).

## 🤝 Contributing

1. Fork the repository
2. Set up a development install(`uv sync --all-extras && pre-commit install`)
3. Create a feature branch (`git checkout -b feature/amazing-feature`)
4. Make your changes
5. Add tests for new functionality
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Use type hints where appropriate
- Ensure all tests pass before submitting

## 📋 Requirements

- Python 3.12+
- **Optional:** Pollinations API key (only needed for premium models)
  - **Free Tier:** Works without any API key using basic models
  - **Premium Tier:** Requires `POLLINATIONS_API_KEY` for advanced models like DeepSeek, Qwen, Mistral

## 🔧 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Try setting PYTHONPATH
PYTHONPATH=. polli run "your task"
```

**API Key Issues:**
```bash
# Check if Pollinations API key is set (optional)
echo $POLLINATIONS_API_KEY

# Check configuration
polli show-config

# Test without API key (should work with basic models)
polli run "Create a simple Python script" --provider pollinations
```

**Permission Errors:**
```bash
# Ensure proper permissions for file operations
chmod +x /path/to/your/project
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Pollinations AI](https://pollinations.ai)** - For providing the powerful AI models that make Polli-Agent possible
- **[Trae-Agent](https://github.com/trae-agent/trae-agent)** - The excellent foundation that Polli-Agent is built upon
- **Anthropic** - For building the [anthropic-quickstart](https://github.com/anthropics/anthropic-quickstarts) project that served as a valuable reference for the tool ecosystem
