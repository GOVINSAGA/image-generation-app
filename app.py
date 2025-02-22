from flask import Flask, render_template, request, Response
import base64
from together import Together
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.getenv('TOGETHER_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Input validation
        if not request.form.get("prompt"):
            return "Prompt is required", 400

        prompt = request.form.get("prompt")

        # Verify API key is available
        if not API_KEY:
            return "API key not configured", 500

        # Initialize the Together API client
        client = Together(api_key=API_KEY)

        # Generate the image
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            width=1024,
            height=768,
            steps=1,
            n=1,
            response_format="b64_json"
        )

        # Decode the Base64 response
        img_data = response.data[0].b64_json
        img_bytes = base64.b64decode(img_data)

        return Response(img_bytes, mimetype='image/png')

    except Exception as e:
        # Log the error (in a production environment, use proper logging)
        print(f"Error generating image: {str(e)}")
        return f"Error generating image: {str(e)}", 500

if __name__ == '__main__':
    # Ensure API key is set
    if not API_KEY:
        print("Warning: TOGETHER_API_KEY environment variable not set")
    
    app.run(debug=False)  # Set debug=False in production