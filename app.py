from flask import Flask, render_template, request, Response
import base64
from together import Together

app = Flask(__name__)

# Replace with your actual API key
API_KEY = "829d5e1ed0596f10ffaacfe222cdf4976b278dbb2d36350698518d336bb620bf"

@app.route('/')
def index():
    # Render a simple form to input your prompt
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get the prompt from the form (or use a default if none provided)
    prompt = request.form.get("prompt") or "[father , son fighting with dragon on mountain, realistic , unreal engine, with american flag]"
    
    # Initialize the Together API client with your API key
    client = Together(api_key=API_KEY)
    
    # Generate the image using Together's API
    response = client.images.generate(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell-Free",
        width=1024,
        height=768,
        steps=1,
        n=1,
        response_format="b64_json"
    )
    
    # Decode the Base64 response to image bytes
    img_data = response.data[0].b64_json
    img_bytes = base64.b64decode(img_data)
    
    # Return the image as a PNG
    return Response(img_bytes, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
