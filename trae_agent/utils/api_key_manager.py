"""API Key management utilities for Polli-Agent."""

import os
import json
from pathlib import Path
from typing import Optional
import click
from rich.console import Console

console = Console()

# Models that require API keys (premium tier)
# Note: Most Pollinations models are free, but some premium models may require API keys
# This list can be updated based on actual API requirements
PREMIUM_MODELS = {
    # Currently, most models are free but API key provides higher rate limits
    # Add specific premium models here as they become available
    "premium-model-example",  # Placeholder - update with actual premium models
}

# File to store API key
API_KEY_FILE = Path.home() / ".pollinations" / "api_key"


def is_premium_model(model_name: str) -> bool:
    """Check if a model requires an API key (premium tier)."""
    return model_name in PREMIUM_MODELS


def get_stored_api_key() -> Optional[str]:
    """Get API key from stored file."""
    try:
        if API_KEY_FILE.exists():
            return API_KEY_FILE.read_text().strip()
    except Exception:
        pass
    return None


def store_api_key(api_key: str) -> bool:
    """Store API key to file."""
    try:
        API_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        API_KEY_FILE.write_text(api_key.strip())
        API_KEY_FILE.chmod(0o600)  # Secure permissions
        return True
    except Exception as e:
        console.print(f"[red]Error storing API key: {e}[/red]")
        return False


def offer_api_key_setup(model_name: str) -> Optional[str]:
    """Offer to set up API key for better performance (optional)."""
    console.print()
    console.print(f"[yellow]💡 Optional: Pollinations API Key[/yellow]")
    console.print(f"Using model '{model_name}' without an API key (free tier).")
    console.print("An API key provides:")
    console.print("  • Higher rate limits")
    console.print("  • Better reliability")
    console.print("  • Priority access")
    console.print()
    console.print("📍 Get your free API key at: [blue]https://auth.pollinations.ai[/blue]")
    console.print()
    
    # Check if user wants to set up API key
    if not click.confirm("Would you like to set up an API key now?", default=False):
        console.print("[green]✅ Continuing without API key (free tier)[/green]")
        return None
    
    return prompt_for_api_key(model_name)


def prompt_for_api_key(model_name: str) -> Optional[str]:
    """Prompt user for API key with helpful information."""
    # Prompt for API key
    api_key = click.prompt(
        "Enter your Pollinations API key",
        type=str,
        hide_input=True,
        confirmation_prompt=False
    )
    
    if not api_key or not api_key.strip():
        console.print("[red]❌ No API key provided[/red]")
        return None
    
    api_key = api_key.strip()
    
    # Ask if user wants to save it
    if click.confirm("Save API key for future use?", default=True):
        if store_api_key(api_key):
            console.print("[green]✅ API key saved successfully![/green]")
        else:
            console.print("[yellow]⚠️  API key not saved, but will be used for this session[/yellow]")
    
    return api_key


def ensure_api_key_available(provider: str, model_name: str, current_api_key: Optional[str]) -> Optional[str]:
    """
    Ensure API key is available for Pollinations providers.
    Returns the API key to use, or None if not available.
    """
    # Only check for Pollinations providers
    if not provider.startswith("pollinations"):
        return current_api_key
    
    # If API key already provided, use it
    if current_api_key:
        return current_api_key
    
    # Check environment variable
    env_key = os.getenv("POLLINATIONS_API_KEY")
    if env_key:
        return env_key
    
    # Check stored API key
    stored_key = get_stored_api_key()
    if stored_key:
        console.print("[green]🔑 Using stored Pollinations API key[/green]")
        return stored_key
    
    # Offer to set up API key for better performance
    return offer_api_key_setup(model_name)


def update_config_with_api_key(config_dict: dict, api_key: str) -> dict:
    """Update configuration dictionary with API key for all Pollinations providers."""
    for provider_name, provider_config in config_dict.get("model_providers", {}).items():
        if provider_name.startswith("pollinations"):
            provider_config["api_key"] = api_key
    return config_dict
