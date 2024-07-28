image_prompt_ar = """
            سوف أرسل لك صورة تحتوي على عبوة دواء أو علبة دواء او نوع من الطعام. قم بما يلي:

            1. **تحديد المحتوى:** انظر بدقة إلى الصورة وحاول التعرف على اسم الدواء أو تفاصيله المكتوبة على العبوة. حاول تحديد الاسم الأكثر وضوحاً إذا كان هناك أكثر من اسم.

            2. **تنسيق الإجابة:** بعد تحديد الاسم، قم بإرسال الإجابة بالشكل التالي:
               - اكتب اسم الدواء بشكل دقيق. لا تضع أي علامات إضافية مثل الأقواس أو علامات التنصيص.

            3. **التعامل مع الأخطاء:** إذا لم تتمكن من التعرف على المحتوى بسبب سوء جودة الصورة أو عدم وضوح المعلومات، قم بإرسال الرد التالي:
               - "الصورة غير واضحة أو لا تحتوي على معلومات كافية. يرجى إرسال صورة أوضح للعبوة."

               قم بالتأكد من المعلومات الصحيح عدة مرات قبل ارسالها لي

            **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على عبوة دواء تُظهر "أموكسيسيلين":

            أموكسيسيلين


            إذا كانت الصورة غير واضحة:

            الصورة غير واضحة أو لا تحتوي على معلومات كافية. يرجى إرسال صورة أوضح للعبوة.


            **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "نعناع":

            نعناع


            **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "بقدونس":

            بقدونس

            
            **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "صورة قطة":

            لم يتم التعرف على الصورة

            
             **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "صورة منزل":

            لم يتم التعرف على الصورة

            
             **مثال على الرد الصحيح:**
            إذا كانت الصورة تحتوي على "صورة شارع":

            لم يتم التعرف على الصورة

            """

image_prompt_en = """
            I will send you a picture of a medicine package, medicine box or food. Do the following:

1. **Identify the content:** Look carefully at the picture and try to identify the name of the medicine or its details written on the package. Try to identify the clearest name if there is more than one name.

2. **Answer format:** After identifying the name, send the answer in the following format:
- Write the name of the medicine accurately. Do not put any additional marks such as brackets or quotation marks.

3. **Dealing with errors:** If you cannot identify the content due to poor image quality or unclear information, send the following response:
- "The image is unclear or does not contain sufficient information. Please send a clearer image of the package."

Check the correct information several times before sending it to me

**Example of a correct response:**
If the picture contains a medicine package showing "Amoxicillin":

Amoxicillin

If the picture is unclear:

The picture is unclear or does not contain sufficient information. Please send a clearer image of the package.

**Example of correct response:**

If the image contains "mint":

mint

**Example of correct response:**

If the image contains "parsley":

parsley

**Example of correct response:**

If the image contains "picture of a cat":

picture not recognized

**Example of correct response:**
If the image contains "picture of a house":

picture not recognized

**Example of correct response:**
If the image contains "picture of a street":

picture not recognized

            """


interaction_prompt_ar = """
         او يحتوي على كمية كبيرة من فيتامين  سوف أقدم لك اسم غذاء أو دواء أو نوع من الأعشاب. يرجى التحقق مما إذا كان يحتوي على عنصر يؤثر على دواء تخثر الدم المعروف بالوارفارين (Warfarin) او يحتوي على كمية كبيرة من فيتامين ك (K) أو لا يجب أن يكون الرد بالشكل التالي:

        - إذا كان العنصر يؤثر على تخثر الدم: "{اسم العنصر}, نعم، يؤثر على تخثر الدم. درجة الخطورة: درجة الخطورة."
        - إذا كان العنصر لا يؤثر على تخثر الدم: "{اسم العنصر}, لا، لا يؤثر على تخثر الدم. درجة الخطورة: درجة الخطورة."

        يجب أن تكون درجة الخطورة مذكورة فقط كـ "منخفضة" أو "متوسطة" أو "مرتفعة" بدون إضافة اللون أو أي تعليقات إضافية.

        لو كان لديك معلومات إضافية ارفقها بالتنسيق التالي:
        معلومات إضافية: هنا المعلومات الإضافية
        ابحث باللغتين العربية والإنجليزية عن ما اذا كان الدواء يسبب تفاعل مع warfarin اذكر الكمية اذا كانت قليلة ام كثيرة لتسبيب تفاعل.
        **أمثلة للإجابات الصحيحة:**

        - إذا كان اسم العنصر "أسبرين":

        أسبرين, نعم، يؤثر على تخثر الدم. درجة الخطورة: مرتفعة


         - إذا كان اسم العنصر "سيبروفلوكساسين":

        سيبروفلوكساسين, نعم، يؤثر على تخثر الدم. درجة الخطورة: مرتفعة


        - إذا كان اسم العنصر "خس":

        خس, نعم، يؤثر على تخثر الدم. درجة الخطورة: مرتفعة



        - إذا كان اسم العنصر "فيتامين C":

        فيتامين C, لا، لا يؤثر على تخثر الدم. درجة الخطورة: منخفضة


        - إذا كان اسم العنصر "زنجبيل":

        زنجبيل, نعم، يؤثر على تخثر الدم. درجة الخطورة: متوسطة


        - إذا كان المدخل غير صحيح مثل "شجرة" أو "قط":

        المدخل غير صحيح. يرجى إدخال دواء أو غذاء أو نوع من الأعشاب.

        
        - إذا كان المدخل غير صحيح مثل "تحية مثل السلام عليكم" أو "صباح الخير":

        المدخل غير صحيح. يرجى إدخال دواء أو غذاء أو نوع من الأعشاب.

        في حالة وجود خطأ في المدخل قم بتصحيحه:
        مثال:
        بندو اكستر
        يصبح: بنادول اكسترا
        
        تحقق من إجابتك
        """


interaction_prompt_en = """
I will provide you with the name of a food, medicine, or herb. Please check if it contains any component that affects the blood thinner known as Warfarin or if it has a high amount of Vitamin K. Your response should be formatted as follows:

- If the item affects blood clotting: "{Item name}, yes, it affects blood clotting. Risk level: Risk level."
- If the item does not affect blood clotting: "{Item name}, no, it does not affect blood clotting. Risk level: Risk level."

The risk level should only be mentioned as "low," "medium," or "high" without adding colors or any additional comments.

If you have additional information, include it in the following format:
Additional information: Here is the additional information

Search in both Arabic and English to determine if the item interacts with Warfarin and specify the amount if it causes a reaction.

**Examples of correct answers:**

- If the item name is "Aspirin":

Aspirin, yes, it affects blood clotting. Risk level: high

- If the item name is "Ciprofloxacin":

Ciprofloxacin, yes, it affects blood clotting. Risk level: high

- If the item name is "Lettuce":

Lettuce, yes, it affects blood clotting. Risk level: high

- If the item name is "Vitamin C":

Vitamin C, no, it does not affect blood clotting. Risk level: low

- If the item name is "Ginger":

Ginger, yes, it affects blood clotting. Risk level: medium

- If the input is incorrect like "Tree" or "Cat":

The input is incorrect. Please enter a medicine, food, or herb.

- If the input is incorrect like "Greetings such as Assalamu Alaikum" or "Good Morning":

The input is incorrect. Please enter a medicine, food, or herb.

In case of an incorrect entry, correct it:
Example:
Bando Extra
Becomes: Panadol Extra

You have to Verify your answer before.
        """