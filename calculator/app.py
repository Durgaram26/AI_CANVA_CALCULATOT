from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
from PIL import Image
import google.generativeai as genai
import base64
import io
import json
from datetime import datetime

app = Flask(__name__)

# Initialize gemini
genai.configure(api_key="API")
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize global variables
canvas = None
response_text = None

def initialize_canvas(width=640, height=480):
    """Initialize a blank canvas"""
    return np.zeros((height, width, 3), dtype=np.uint8)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_drawing', methods=['POST'])
def analyze_drawing():
    try:
        # Get the image data from the request
        data = request.json
        image_data = data['image'].split(',')[1]  # Remove the data URL prefix
        
        # Convert base64 to image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Send to Gemini for analysis
        response = model.generate_content([
            "This is a math problem. Please solve it and explain the solution step by step. "
            "If you see an equation, write out the complete solution. "
            "If the equation is 5 + 5 = ?, solve it as: 5 + 5 = 10", 
            image
        ])
        
        response_text = response.text if response else "Could not analyze the image"
        return jsonify({
            'status': 'success', 
            'response': response_text,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    except Exception as e:
        print(f"Error analyzing drawing: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error analyzing drawing: {str(e)}'})

@app.route('/clear_canvas')
def clear_canvas():
    global canvas
    canvas = initialize_canvas()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    canvas = initialize_canvas()
    app.run(debug=True)