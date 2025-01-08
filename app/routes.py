import base64
import os
import uuid

import requests
from flask import render_template, redirect, url_for, flash, request
from openai import OpenAI
from app.prompts import *
from app import app

API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')
client = OpenAI(api_key=API_KEY)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {client.api_key}"
}

lang = ""
@app.route('/', methods=['GET', 'POST'])
def index():
    lang = "ar"
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            original_filename = file.filename
            extension = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{extension}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'] + 'images', unique_filename)
            file.save(file_path)
            try:
                product_name = get_name_from_image(file_path, "ar")
                effect, info = get_interaction_from_name(product_name, "ar")
                return render_template('result.html', result=effect, name=product_name, info=info)
            except Exception as e:
                print(f"Error: {e}")
                flash("خطأ في معالجة الصورة. حاول مرة أخرى.", "danger")
        elif 'text' in request.form and request.form['text'].strip() != '':
            text = request.form['text'].strip().lower()
            effect, info = get_interaction_from_name(text, "ar")
            return render_template('result.html', result=effect, name=text.capitalize(), info=info)
        elif 'voice' in request.form and request.form['voice'].strip() != '':
            voice_data = request.form['voice']
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'] + 'voices', f"{uuid.uuid4()}.wav")
            with open(audio_path, "wb") as audio_file:
                audio_file.write(base64.b64decode(voice_data.split(',')[1]))
            try:
                transcript = recognize_speech(audio_path, "ar")
                effect, info = get_interaction_from_name(transcript, "ar")
                return render_template('result.html', result=effect, name=transcript, info=info)
            except Exception as e:
                print(f"Error: {e}")
                flash("خطأ في معالجة الصوت. حاول مرة أخرى.", "danger")
        else:
            print("here")
            return render_template('index.html', error="يرجى تقديم مدخل لرؤية النتيجة.")
    return render_template('index.html')


@app.route('/en', methods=['GET', 'POST'])
def eng_index():
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            original_filename = file.filename
            extension = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{extension}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'] + 'images', unique_filename)
            file.save(file_path)
            try:
                product_name = get_name_from_image(file_path, "en")
                effect, info = get_interaction_from_name(product_name, "en")
                return render_template('en/result.html', result=effect, name=product_name, info=info)
            except Exception as e:
                print(f"Error: {e}")
                flash("Error at processing, please try again later.", "danger")
        elif 'text' in request.form and request.form['text'].strip() != '':
            text = request.form['text'].strip().lower()
            effect, info = get_interaction_from_name(text, "en")
            return render_template('en/result.html', result=effect, name=text.capitalize(), info=info)
        elif 'voice' in request.form and request.form['voice'].strip() != '':
            voice_data = request.form['voice']
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'] + 'voices', f"{uuid.uuid4()}.wav")
            with open(audio_path, "wb") as audio_file:
                audio_file.write(base64.b64decode(voice_data.split(',')[1]))
            try:
                transcript = recognize_speech(audio_path, "en")
                effect, info = get_interaction_from_name(transcript, "en")
                return render_template('en/result.html', result=effect, name=transcript, info=info)
            except Exception as e:
                print(f"Error: {e}")
                flash("Error at processing the voice, please try again later.", "danger")
        else:
            print("here")
            return render_template('index.html', error="Please provide in input to be processed.")
    return render_template('en/index.html')

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_interaction_from_name(name, lang):
    if lang == "en":
        prompt = interaction_prompt_en
    else:
        prompt = interaction_prompt_ar

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": name
            }
        ],
        "temperature" : 0,
        "max_tokens": 80
    }

    

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()['choices'][0]['message']['content'].strip()
    print(response.text)
    
    if lang == "ar":
        try:
            effect, info = result.split("معلومات إضافية:", 1)
            effect = effect.strip()
            info = info.strip()
        except ValueError:
            effect = result
            info = ".المعلومات إضافية غير متوفرة"
    else:
        try:
            effect, info = result.split("Additional information:", 1)
            effect = effect.strip()
            info = info.strip()
        except ValueError:
            effect = result
            info = "Additional information is not available:"

    return effect, info


def get_name_from_image(image_path, lang):
    if lang == "en":
        prompt = image_prompt_en
    else:
        prompt = image_prompt_ar
    
    base64_image = encode_image(image_path)
    os.remove(image_path)
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "temperature" : 0,
        "max_tokens": 20
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content'].strip()


def recognize_speech(audio_path, lang):
    if lang == "en":
        prompt = "Match English language."
    else:
        prompt = "تعرف على اللغة العربية"
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
            prompt=prompt
        )
    print("text from transaction: ", transcription)
    os.remove(audio_path)
    return transcription.strip()
