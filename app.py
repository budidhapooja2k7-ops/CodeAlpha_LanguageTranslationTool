from flask import Flask, render_template, request
from deep_translator import GoogleTranslator

app = Flask(__name__)

history = []

languages = {
    "auto": "Auto Detect",
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-CN": "Chinese",
    "ar": "Arabic"
}


@app.route("/", methods=["GET", "POST"])
def translate():

    translated_text = ""
    error = ""

    text = ""
    source_lang = "auto"
    target_lang = "en"

    if request.method == "POST":

        # Clear translation history
        if request.form.get("clear_history") == "yes":

            history.clear()

        else:

            text = request.form.get("text", "").strip()

            source_lang = request.form.get(
                "source",
                "auto"
            )

            target_lang = request.form.get(
                "target",
                "en"
            )

            if not text:

                error = "Please enter some text to translate."

            elif len(text) > 5000:

                error = "Please keep your text under 5000 characters."

            elif (
                source_lang == target_lang
                and source_lang != "auto"
            ):

                translated_text = text

            else:

                try:

                    translator = GoogleTranslator(
                        source=source_lang,
                        target=target_lang
                    )

                    translated_text = translator.translate(text)

                    if not translated_text:

                        error = "No translation was returned."

                    else:



                     history.insert(
    0,
    {
        "original": text,
        "translation": translated_text,
        "source_code": source_lang,
        "target_code": target_lang,
        "source_name": languages.get(
            source_lang,
            source_lang
        ),
        "target_name": languages.get(
            target_lang,
            target_lang
        )
    }
)

                        # Keep only latest 5 translations
                    if len(history) > 5:
                            history.pop()

                except Exception as e:

                    print("Translation error:", e)

                    error = (
                        "Translation failed. "
                        "Please check your internet connection "
                        "and try again."
                    )

    return render_template(
        "index.html",
        translated_text=translated_text,
        error=error,
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        languages=languages,
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)