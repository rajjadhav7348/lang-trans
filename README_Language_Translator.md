
# 🌐 Language Translator Web App

This is a simple language translation web application built using **Flask**, **Flask-Ngrok**, and **Google Translate API** (`googletrans`).

## 🚀 Features

- Translate text between over 100 languages.
- Choose source and target languages from dropdowns.
- Copy translated text to clipboard.
- Listen to the translated text using browser speech synthesis.

## 🧰 Requirements

Install the required packages:

```bash
!pip install -q flask-ngrok googletrans==4.0.0-rc1
```

## ⚙️ How to Run in Google Colab

1. **Suppress debug inspection warning**:
    ```python
    import logging
    logging.getLogger('google.colab._debugpy_repr').setLevel(logging.ERROR)
    ```

2. **Define and launch Flask app**:
    ```python
    try:
        app  # check if already defined
    except NameError:
        from flask import Flask, render_template_string, request
        from flask_ngrok import run_with_ngrok
        from googletrans import Translator, LANGUAGES

        app = Flask(__name__)
        run_with_ngrok(app)
        translator = Translator()

        HTML_TEMPLATE = """[HTML code from the main script here]"""

        @app.route("/", methods=["GET", "POST"])
        def index():
            translated_text = ""
            if request.method == "POST":
                text = request.form["text"]
                src_lang = request.form["src_lang"]
                dest_lang = request.form["dest_lang"]
                if text:
                    translated = translator.translate(text, src=src_lang, dest=dest_lang)
                    translated_text = translated.text
            return render_template_string(HTML_TEMPLATE, languages=LANGUAGES, translated_text=translated_text)

        app.run()
    else:
        print("✅ App is already running. If you want to re-run it, restart the runtime (Runtime > Restart runtime).")
    ```

## 📋 Notes

- `googletrans` is a free and unofficial API. It may sometimes be unreliable due to changes on Google's side.
- Works best in **Google Colab** with Ngrok tunneling for easy public access.

## 📎 Credits

- [Flask](https://flask.palletsprojects.com/)
- [Flask-Ngrok](https://pypi.org/project/flask-ngrok/)
- [Googletrans (Unofficial API)](https://pypi.org/project/googletrans/)
