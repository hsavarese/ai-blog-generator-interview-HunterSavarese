import os
import sys
import pytest
from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Ensure we have required environment variables
    assert os.getenv('OPENAI_API_KEY'), "OPENAI_API_KEY not found in environment variables"
    
    # Create generated_posts directory if it doesn't exist
    if not os.path.exists('generated_posts'):
        os.makedirs('generated_posts') 
