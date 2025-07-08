from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Language Translation Tool</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; padding: 2rem; }
        .box { max-width: 600px; margin: auto; background: #fff; padding: 1.5rem; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        textarea, select, button { width: 100%; margin-top: 10px; padding: 10px; font-size: 1rem; border-radius: 4px; border: 1px solid #ccc; }
        button { cursor: pointer; background: #007bff; color: white; border: none; }
        button:hover { background: #0056b3; }
        #output { margin-top: 15px; background: #f9f9f9; padding: 10px; border-radius: 6px; min-height: 80px; white-space: pre-wrap; }
        .btn-group { display: flex; gap: 10px; margin-top: 10px; }
        .btn-group button { flex: 1; }
        label { font-weight: bold; margin-top: 10px; display: block; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Language Translation Tool</h2>
        <form id="translateForm">
            <label for="sourceLang">Source Language</label>
            <select id="sourceLang" name="sourceLang">
                <option value="auto">Auto Detect</option>
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="fr">French</option>
                <option value="es">Spanish</option>
                <option value="de">German</option>
                <option value="zh">Chinese</option>
                <option value="ja">Japanese</option>
                <option value="ru">Russian</option>
                <option value="ar">Arabic</option>
                <option value="pt">Portuguese</option>
                <option value="bn">Bengali</option>
                <option value="pa">Punjabi</option>
                <option value="mr">Marathi</option>
                <option value="ta">Tamil</option>
                <option value="ur">Urdu</option>
            </select>

            <label for="targetLang">Target Language</label>
            <select id="targetLang" name="targetLang" required>
                <option value="hi">Hindi</option>
                <option value="en" selected>English</option>
                <option value="fr">French</option>
                <option value="es">Spanish</option>
                <option value="de">German</option>
                <option value="zh">Chinese</option>
                <option value="ja">Japanese</option>
                <option value="ru">Russian</option>
                <option value="ar">Arabic</option>
                <option value="pt">Portuguese</option>
                <option value="bn">Bengali</option>
                <option value="pa">Punjabi</option>
                <option value="mr">Marathi</option>
                <option value="ta">Tamil</option>
                <option value="ur">Urdu</option>
            </select>

            <label for="textInput">Text to Translate</label>
            <textarea id="textInput" name="textInput" rows="5" placeholder="Enter text here..." required></textarea>
            <button type="submit">Translate</button>
        </form>
        <div id="output" aria-live="polite"></div>
        <div class="btn-group">
            <button onclick="copyText()" type="button">Copy</button>
            <button onclick="speakText()" type="button">Speak</button>
        </div>
    </div>

<script>
document.getElementById('translateForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const source = document.getElementById('sourceLang').value;
    const target = document.getElementById('targetLang').value;
    const text = document.getElementById('textInput').value.trim();

    if (!text) {
        alert("Please enter some text to translate.");
        return;
    }

    document.getElementById('output').textContent = "Translating...";
    try {
        const res = await fetch('/translate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({source, target, text})
        });

        const data = await res.json();
        if(data.translatedText){
            document.getElementById('output').textContent = data.translatedText;
        } else {
            document.getElementById('output').textContent = "Translation failed.";
        }
    } catch (error) {
        document.getElementById('output').textContent = "Error during translation.";
        console.error(error);
    }
});

function copyText() {
    const text = document.getElementById('output').textContent;
    if (!text) {
        alert("Nothing to copy!");
        return;
    }
    navigator.clipboard.writeText(text).then(() => {
        alert("Copied to clipboard!");
    }).catch(() => {
        alert("Failed to copy!");
    });
}

function speakText() {
    const text = document.getElementById('output').textContent;
    if (!text) {
        alert("Nothing to speak!");
        return;
    }
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = document.getElementById('targetLang').value;
    window.speechSynthesis.speak(speech);
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    source = data.get('source', 'auto')
    target = data.get('target', 'en')

    url = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_API_KEY}"
    payload = {
        "q": text,
        "target": target,
        "format": "text"
    }
    if source != "auto":
        payload["source"] = source

    response = requests.post(url, json=payload)
    result = response.json()

    if "error" in result:
        return jsonify({"translatedText": "", "error": result["error"]["message"]})

    translated = result["data"]["translations"][0]["translatedText"]
    return jsonify({"translatedText": translated})

if __name__ == '__main__':
    app.run(debug=True)
