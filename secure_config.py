"""
Secure API Key Management for Streamlit Hosting
This module ensures API keys are only accessed server-side and never exposed to clients.
"""
import os
import streamlit as st
from typing import Optional


def get_gemini_api_key() -> Optional[str]:
    """
    Securely retrieve Gemini API key from server-side sources only.
    
    Priority order:
    1. Streamlit secrets (recommended for Streamlit Cloud)
    2. Environment variable (for Docker/local deployment)
    
    Returns:
        API key string if found, None otherwise
        
    Security Notes:
        - Never exposes API key to client-side code
        - Never uses user input or frontend storage
        - Safe for production hosting
    """
    # Try Streamlit secrets first (best for Streamlit Cloud)
    try:
        if hasattr(st, 'secrets'):
            api_key = st.secrets.get("GEMINI_API_KEY")
            if api_key:
                return api_key
    except (AttributeError, KeyError, Exception):
        # Streamlit secrets not available or key not found
        pass
    
    # Fallback to environment variable (for Docker/local)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    return None


def validate_api_key(api_key: Optional[str]) -> bool:
    """
    Validate that an API key exists and is not empty.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    return api_key is not None and len(api_key.strip()) > 0


def get_gemini_api_key_safe() -> str:
    """
    Get Gemini API key with validation.
    Raises an error if key is not found (for production safety).
    
    Returns:
        API key string
        
    Raises:
        ValueError: If API key is not configured
    """
    api_key = get_gemini_api_key()
    if not validate_api_key(api_key):
        raise ValueError(
            "GEMINI_API_KEY not found. Please configure it in:\n"
            "1. Streamlit Cloud: Add to Settings > Secrets\n"
            "2. Local: Create .streamlit/secrets.toml with GEMINI_API_KEY = 'your-key'\n"
            "3. Docker: Set GEMINI_API_KEY environment variable"
        )
    return api_key

