#!/usr/bin/env python3
"""
Entry point script for Cognitive Career Recommendation System
Run this script to start the Flask application
"""

import os
import sys

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def setup_nltk():
    """Setup NLTK models if needed"""
    try:
        import nltk
        import ssl
        
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
            
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        return True
    except Exception as e:
        print(f"⚠ NLTK setup warning: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🧠 Cognitive Career & Job Recommendation System")
    print("=" * 60)
    
    # Setup NLTK data
    setup_nltk()
    
    print("🚀 Starting Flask Application")
    print("-" * 30)
    print("📍 Access the application at: http://localhost:5000")
    print("📍 Use Ctrl+C to stop the server")
    print("-" * 50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"✗ Error importing Flask app: {e}")
        print("Please make sure all dependencies are installed correctly.")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error starting application: {e}")
        sys.exit(1)