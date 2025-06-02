#!/usr/bin/env python3
"""
Image Tagger Web Application

A web app for crawling websites for images, viewing and tagging them.
"""

import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Create storage directory if it doesn't exist
    os.makedirs(app.config['IMAGE_STORAGE_PATH'], exist_ok=True)
    
    # Run the app in debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)
