#!/usr/bin/env python3
"""
Startup script for Railway deployment
"""
import os
import sys

# Add the Backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Backend'))

# Import and run the Flask app
from Backend.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
