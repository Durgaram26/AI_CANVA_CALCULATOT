# Calculator Drawing Analyzer

A small Flask app that accepts hand-drawn math on a canvas, sends the image to Google Gemini (Generative AI) for OCR and step-by-step solution, and returns the result as JSON.

## Features

- Web UI (`templates/index.html`) with a drawable canvas.
- Endpoint `/analyze_drawing` to POST a base64 image and receive a solved math explanation from Gemini.
- Simple `/clear_canvas` endpoint to reset the server-side canvas.

## Files

- `app.py` — Flask application and API endpoints.
- `templates/index.html` — Front-end drawing canvas (served at `/`).

## Dependencies

- Python 3.8+ (3.10 recommended)
- Flask
- OpenCV (`opencv-python`)
- Pillow
- NumPy
- `google-generativeai` (Gemini client)

Install dependencies with:

```bash
pip install flask opencv-python pillow numpy google-generativeai
```

## Configuration

The app uses the Google Generative AI client. Set your API key before running — either modify `app.py` to read from environment variables or replace the placeholder:

```python
# in app.py
genai.configure(api_key="YOUR_API_KEY")
```

Important: Do not commit your API key to source control.

## Running locally

1. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. Install dependencies (see above).

3. Start the Flask app:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000/` in your browser and draw a math problem on the canvas. Click the analyze button to send the image to Gemini and receive the solution.

## API

- POST `/analyze_drawing` — JSON body: `{ "image": "data:image/png;base64,<base64-data>" }`
  - Response: `{ "status": "success", "response": "<text>", "timestamp": "YYYY-MM-DD HH:MM:SS" }`
- GET `/clear_canvas` — Resets the server-side canvas. Response: `{ "status": "success" }`

## Notes

- The app sends the PIL image directly to Gemini using the `model.generate_content([..., image])` pattern in `app.py`. Ensure your `google-generativeai` package version supports image inputs.
- For deployment, replace the hard-coded API key with secure environment variable handling and enable proper rate-limiting and error handling.

## License

Add a `LICENSE` file if you plan to publish this project. 