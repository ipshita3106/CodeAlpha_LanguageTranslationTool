import requests
import html

API_URL = "https://api.mymemory.translated.net/get"


def translate_text(text, source_language, target_language):

    if not text.strip():
        raise ValueError("Please enter some text.")

    if len(text.encode("utf-8")) > 500:
        raise ValueError("Text is too long. Maximum 500 bytes per request.")

    params = {
        "q": text,
        "langpair": f"{source_language}|{target_language}"
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("responseStatus") != 200:
            raise Exception(
                data.get("responseDetails", "Translation failed.")
            )

        translated_text = data["responseData"]["translatedText"]

        return html.unescape(translated_text)

    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Please try again.")

    except requests.exceptions.RequestException:
        raise Exception("Unable to connect to the translation service.")
