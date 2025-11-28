"""
AI Chat Application using local llama.cpp model via OpenAI-compatible API.

This module provides a Flask web server that serves a ChatGPT-like interface
for interacting with a local AI model.
"""

import os
import doctest
from typing import Optional
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from openai import APIError, APIConnectionError

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for frontend-backend communication

# Load configuration from environment variables
BASE_URL = os.getenv("BASE_URL", "http://localhost:12434/engines/llama.cpp/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "ai/smollm2")
API_KEY = os.getenv("API_KEY", "not-needed")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Initialize the OpenAI client with local base URL
try:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
except Exception as e:
    print(f"Warning: Failed to initialize OpenAI client: {e}")
    client = None


def generate_response(prompt: str, model: Optional[str] = None, 
                     max_tokens: Optional[int] = None, 
                     temperature: Optional[float] = None) -> dict:
    """
    Generate a response from local llama.cpp model.
    
    Args:
        prompt (str): The input prompt/question to send to the model.
        model (Optional[str]): Model name to use (defaults to MODEL_NAME from env).
        max_tokens (Optional[int]): Maximum tokens to generate (defaults to MAX_TOKENS from env).
        temperature (Optional[float]): Temperature for generation (defaults to TEMPERATURE from env).
        
    Returns:
        dict: Response dictionary with keys:
            - 'success' (bool): Whether the generation was successful.
            - 'message' (str): The generated text content or empty string on failure.
            - 'model' (str): The model name used (only on success).
            - 'error' (str): Error message description (only on failure).
        
    Examples:
        >>> # Test with empty prompt (edge case)
        >>> result = generate_response("")
        >>> 'success' in result
        True
        >>> result['success']
        False
        >>> 'error' in result
        True
        
        >>> # Test with valid prompt structure
        >>> result = generate_response("test")
        >>> 'success' in result
        True
        >>> 'message' in result
        True
        >>> isinstance(result['message'], str)
        True
    """
    # Edge case: Empty prompt
    if not prompt or not prompt.strip():
        return {
            'success': False,
            'message': '',
            'error': 'Prompt cannot be empty'
        }
    
    # Edge case: Client not initialized
    if client is None:
        return {
            'success': False,
            'message': '',
            'error': 'OpenAI client not initialized. Please check your configuration.'
        }
    
    # Use provided parameters or fall back to environment defaults
    model_name = model or MODEL_NAME
    tokens = max_tokens or MAX_TOKENS
    temp = temperature if temperature is not None else TEMPERATURE
    
    try:
        # Create a chat completion using local model
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt.strip()}
            ],
            max_tokens=tokens,
            temperature=temp
        )
        
        # Extract and return the response
        message_content = response.choices[0].message.content
        
        return {
            'success': True,
            'message': message_content,
            'model': model_name
        }
        
    except APIConnectionError as e:
        return {
            'success': False,
            'message': '',
            'error': f'Connection error: Unable to connect to the model server at {BASE_URL}. Please ensure the server is running.'
        }
    except APIError as e:
        return {
            'success': False,
            'message': '',
            'error': f'API error: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': '',
            'error': f'Unexpected error: {str(e)}'
        }


@app.route('/')
def index():
    """
    Serve the main HTML page.

    Returns:
        Response: Flask response object containing the index.html file.
    """
    return send_from_directory('.', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint for chat completion.
    
    Receives a JSON payload with the prompt and optional parameters, calls the
    model generation function, and returns the result.

    Args:
        None (Uses Flask request context).

    Expected JSON payload:
        {
            "prompt": "user's message",
            "model": "optional model name",
            "max_tokens": optional integer,
            "temperature": optional float
        }
    
    Returns:
        Response: JSON response containing:
            - success (bool): Whether the request was successful.
            - message (str): The response text.
            - error (str): Error message if applicable.
        Status Code:
            - 200: Success.
            - 400: Bad Request (missing prompt).
            - 500: Server Error.
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                'success': False,
                'message': '',
                'error': 'Missing required field: prompt'
            }), 400
        
        prompt = data['prompt']
        model = data.get('model')
        max_tokens = data.get('max_tokens')
        temperature = data.get('temperature')
        
        result = generate_response(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        status_code = 200 if result['success'] else 500
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '',
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint.

    Provides the current status of the application and configuration details.

    Args:
        None.

    Returns:
        Response: JSON response containing:
            - status (str): "healthy".
            - base_url (str): Configured model API base URL.
            - model (str): Configured model name.
            - client_initialized (bool): Whether the OpenAI client is active.
        Status Code: 200
    """
    return jsonify({
        'status': 'healthy',
        'base_url': BASE_URL,
        'model': MODEL_NAME,
        'client_initialized': client is not None
    }), 200


if __name__ == "__main__":
    # Run doctests
    doctest.testmod(verbose=True)
    
    # Get Flask configuration
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    
    print(f"Starting Flask server on {host}:{port}")
    print(f"Base URL: {BASE_URL}")
    print(f"Model: {MODEL_NAME}")
    print(f"Client initialized: {client is not None}")
    
    app.run(host=host, port=port, debug=debug)
