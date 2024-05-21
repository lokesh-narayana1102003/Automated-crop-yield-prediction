from googletrans import Translator

from flask import Flask, render_template, request, send_file,redirect
import numpy as np
import pickle
from flask_babel import Babel
import requests


app = Flask(__name__)
@app.route('/change_language', methods=['POST'])
def change_language():
    language = request.form['language']
    if language in app.config['LANGUAGES']:
        translator = Translator()
        translations = translator.translate(texts_to_translate, dest=language)

        # Store the translations in session or cookies
        session['translations'] = translations
        session['language'] = language

    return redirect(url_for('index'))
from flask import g

@app.before_request
def before_request():
    g.translator = Translator()

@app.template_global()
def translate(text):
    if 'translations' in session:
        translations = session['translations']
        for translation in translations:
            if translation.origin == text:
                return translation.text
    return text
@app.before_request
def before_request():
    if 'language' in session:
        language = session['language']
        translations = []

        for text in texts_to_translate:
            translation = g.translator.translate(text, dest=language)
            translations.append(translation)

        session['translations'] = translations


if __name__ == "__main__":
    app.run(host="0.0.0.0")

