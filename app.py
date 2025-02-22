from flask import Flask, render_template, request, Response
import base64
from together import Together
import os
from dotenv import load_dotenv
import re

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv('TOGETHER_API_KEY')

def contains_inappropriate_content(prompt):
    """Check if the prompt contains inappropriate content"""
    inappropriate_terms = [
        'nude', 'naked', 'nsfw', 'xxx', 'porn', 'sexual',
        'explicit', 'adult', '18+', 'erotic', 'leaked',
    ]
    
    prompt_lower = prompt.lower()
    
    for term in inappropriate_terms:
        if term in prompt_lower:
            return True
            
    problematic_patterns = [
        r'\b(18|19|20|21)\s*\+',
        r'nsfw',
        r'xxx',
    ]
    
    for pattern in problematic_patterns:
        if re.search(pattern, prompt_lower):
            return True
    
    return False

def sanitize_prompt(prompt):
    """Sanitize the prompt by adding safety terms"""
    safety_terms = [
        "safe for work",
        "family friendly",
        "appropriate content only",
        "pg rated",
        "high quality",
        "detailed",
        "4k"
    ]
    
    sanitized_prompt = f"{prompt}, {', '.join(safety_terms)}"
    return sanitized_prompt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if not request.form.get("prompt"):
            return "Prompt is required", 400

        prompt = request.form.get("prompt")
        
        if contains_inappropriate_content(prompt):
            return "Inappropriate content detected. Please modify your prompt.", 400
        
        safe_prompt = sanitize_prompt(prompt)
        
        client = Together(api_key=API_KEY)
        
        # Updated parameters to comply with API limitations
        response = client.images.generate(
            prompt=safe_prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            width=1024,
            height=1024,
            steps=4,  # Maximum allowed steps
            n=1,
            response_format="b64_json",
            cfg_scale=7.5,  # Keeping this for better prompt adherence
        )
        
        img_data = response.data[0].b64_json
        img_bytes = base64.b64decode(img_data)
        
        return Response(img_bytes, mimetype='image/png')

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return f"Error generating image: {str(e)}", 500

if __name__ == '__main__':
    if not API_KEY:
        print("Warning: TOGETHER_API_KEY environment variable not set")
    app.run(debug=False)