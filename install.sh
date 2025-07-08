#!/bin/bash

# Polli-Agent Installation Script
# This script installs Polli-Agent globally so you can use the 'polli' command anywhere

set -e

echo "🌸 Installing Polli-Agent..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed."
    echo "Please install pip and try again."
    exit 1
fi

# Use pip3 if available, otherwise pip
PIP_CMD="pip"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
fi

echo "📦 Installing Polli-Agent with $PIP_CMD..."
$PIP_CMD install -e .

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 You can now use Polli-Agent globally:"
echo "   polli run \"Create a Python script\""
echo "   polli interactive"
echo "   polli --help"
echo ""
echo "🔑 For premium models, get your API key at: https://auth.pollinations.ai"
echo ""
echo "Happy coding with Polli-Agent! 🌸"
