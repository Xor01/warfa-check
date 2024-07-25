import base64
import os
import uuid

import requests
from flask import render_template, redirect, url_for, flash, request
from openai import OpenAI

from app import app

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {client.api_key}"
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            original_filename = file.filename
            extension = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{extension}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'] + 'images', unique_filename)
            file.save(file_path)
            try:
                product_name = get_name_from_image(file_path)
                effect, info = get_interaction_from_name(product_name)
                return render_template('result.html', result=effect, name=product_name, info=info)
            except Exception as e:
                print(f"Error: {e}")
                flash("خطأ في معالجة الصورة. حاول مرة أخرى.", "danger")
        elif 'text' in request.form and request.form['text'].strip() != '':
            text = request.form['text'].strip().lower()
            effect, info = get_interaction_from_name(text)
            return render_template('result.html', result=effect, name=text.capitalize(), info=info)
        elif 'voice' in request.form and request.form['voice'].strip() != '':
            voice_data = request.form['voice']
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'] + 'voices', f"{uuid.uuid4()}.wav")
            with open(audio_path, "wb") as audio_file:
                audio_file.write(base64.b64decode(voice_data.split(',')[1]))
            try:
                transcript = recognize_speech(audio_path)
                effect, info = get_interaction_from_name(transcript)
                return render_template('result.html', result=effect, name=transcript, info=info)
            except Exception as e:
                print(f"Error: {e}")
                flash("خطأ في معالجة الصوت. حاول مرة أخرى.", "danger")
        else:
            print("here")
            return render_template('index.html', error="يرجى تقديم مدخل لرؤية النتيجة.")
    return render_template('index.html')


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_interaction_from_name(name):
    prompt = """
        سوف أقدم لك اسم غذاء أو دواء أو نوع من الأعشاب. يرجى التحقق مما إذا كان يحتوي على عنصر يؤثر على دواء تخثر الدم المعروف بالوارفارين أم لا يجب أن يكون الرد بالشكل التالي:

        - إذا كان العنصر يؤثر على تخثر الدم: "{اسم العنصر}, نعم، يؤثر على تخثر الدم. درجة الخطورة: درجة الخطورة."
        - إذا كان العنصر لا يؤثر على تخثر الدم: "{اسم العنصر}, لا، لا يؤثر على تخثر الدم. درجة الخطورة: درجة الخطورة."

        يجب أن تكون درجة الخطورة مذكورة فقط كـ "منخفضة" أو "متوسطة" أو "مرتفعة" بدون إضافة اللون أو أي تعليقات إضافية.

        لو كان لديك معلومات إضافية ارفقها بالتنسيق التالي:
        معلومات إضافية: هنا المعلومات الإضافية
        ابحث باللغتين العربية والإنجليزية عن ما اذا كان الدواء يسبب تفاعل مع warfarin اذكر الكمية اذا كانت قليلة ام كثيرة لتسبيب تفاعل.
        **أمثلة للإجابات الصحيحة:**

        - إذا كان اسم العنصر "أسبرين":
        ```
        أسبرين, نعم، يؤثر على تخثر الدم. درجة الخطورة: مرتفعة
        ```

         - إذا كان اسم العنصر "سيبروفلوكساسين":
        ```
        سيبروفلوكساسين, نعم، يؤثر على تخثر الدم. درجة الخطورة: مرتفعة
        ```


        - إذا كان اسم العنصر "فيتامين C":
        ```
        فيتامين C, لا، لا يؤثر على تخثر الدم. درجة الخطورة: منخفضة
        ```

        - إذا كان اسم العنصر "زنجبيل":
        ```
        زنجبيل, نعم، يؤثر على تخثر الدم. درجة الخطورة: متوسطة
        ```

        - إذا كان المدخل غير صحيح مثل "شجرة" أو "قط":
        ```
        المدخل غير صحيح. يرجى إدخال دواء أو غذاء أو نوع من الأعشاب.
        ```
        
        - إذا كان المدخل غير صحيح مثل "تحية مثل السلام عليكم" أو "صباح الخير":
        ```
        المدخل غير صحيح. يرجى إدخال دواء أو غذاء أو نوع من الأعشاب.
        ```
        في حالة وجود خطأ في المدخل قم بتصحيحه:
        مثال:
        بندو اكستر
        يصبح: بنادول اكسترا
        
        تحقق من إجابتك
        """
        

    payload = {
        "model": "gpt-4o",
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
    try:
        effect, info = result.split("معلومات إضافية:", 1)
        effect = effect.strip()
        info = info.strip()
    except ValueError:
        effect = result
        info = ".المعلومات إضافية غير متوفرة"

    return effect, info


def get_name_from_image(image_path):
    prompt = """
            سوف أرسل لك صورة تحتوي على عبوة دواء أو علبة دواء. قم بما يلي:

            1. **تحديد المحتوى:** انظر بدقة إلى الصورة وحاول التعرف على اسم الدواء أو تفاصيله المكتوبة على العبوة. حاول تحديد الاسم الأكثر وضوحاً إذا كان هناك أكثر من اسم.

            2. **تنسيق الإجابة:** بعد تحديد الاسم، قم بإرسال الإجابة بالشكل التالي:
               - اكتب اسم الدواء بشكل دقيق. لا تضع أي علامات إضافية مثل الأقواس أو علامات التنصيص.

            3. **التعامل مع الأخطاء:** إذا لم تتمكن من التعرف على المحتوى بسبب سوء جودة الصورة أو عدم وضوح المعلومات، قم بإرسال الرد التالي:
               - "الصورة غير واضحة أو لا تحتوي على معلومات كافية. يرجى إرسال صورة أوضح للعبوة."

               قم بالتأكد من المعلومات الصحيح عدة مرات قبل ارسالها لي

            **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على عبوة دواء تُظهر "أموكسيسيلين":
            ```
            أموكسيسيلين
            ```

            إذا كانت الصورة غير واضحة:
            ```
            الصورة غير واضحة أو لا تحتوي على معلومات كافية. يرجى إرسال صورة أوضح للعبوة.
            ```

            **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "نعناع":
            ```
            نعناع
            ```

            **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "بقدونس":
            ```
            بقدونس
            ```
            
            **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "صورة قطة":
            ```
            لم يتم التعرف على الصورة
            ```
            
             **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "صورة منزل":
            ```
            لم يتم التعرف على الصورة
            ```
            
             **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "صورة شارع":
            ```
            لم يتم التعرف على الصورة
            ```
            """
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


def recognize_speech(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
            prompt="حاول التعرف على اللغة العربية اولا، في حالة فشلك انتقل للغة الانجليزية"
        )
    print("text from transaction: ", transcription)
    os.remove(audio_path)
    return transcription
