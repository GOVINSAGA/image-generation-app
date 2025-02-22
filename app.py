from flask import Flask, render_template, request, Response
import base64
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv('TOGETHER_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if not request.form.get("prompt"):
            return "Prompt is required", 400

        prompt = request.form.get("prompt")
        
        # Enhanced API parameters for better quality
        client = Together(api_key=API_KEY)
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            width=1024,  # Larger size for better detail
            height=1024,
            steps=30,    # More steps for better quality
            n=1,
            response_format="b64_json",
            # Additional parameters for quality
            cfg_scale=7.5,  # Controls how closely the image follows the prompt (default is 7.0)
            scheduler="DDIM",  # Different scheduler can affect quality
            style_preset="enhance",  # Can be used if supported by the model
            seed=None  # Random seed for variation
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