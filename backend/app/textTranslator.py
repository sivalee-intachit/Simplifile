import os
import requests
from extractData import *

translator_api_key = "285e0d0d3d7d48a28e5a7bf0b45d4762"
translator_endpoint = "https://api.cognitive.microsofttranslator.com/"

# Function to translate text
def translate_text(text, target_language="es"):
    headers = {
        'Ocp-Apim-Subscription-Key': translator_api_key,
        'Ocp-Apim-Subscription-Region': 'eastus',  # Specify your region
        'Content-type': 'application/json',
        'X-ClientTraceId': str(os.urandom(16))
    }
    translator_url = f"{translator_endpoint}/translate?api-version=3.0&to={target_language}"
    body = [{'text': text}]
    
    response = requests.post(translator_url, headers=headers, json=body)
    
    if response.status_code == 200:
        translations = response.json()
        return translations[0]['translations'][0]['text']
    else:
        print(f"Error in translation: {response.status_code}, {response.text}")
        return None

def getTranslated_text():
    return translated_text

extracted_text = getExtracted_Text()

#ask user for target language
target_language = input("Enter the langauge code you want the text to be translated to: e.g. es for Spanish, fr for French, etc. ")

#translate the text to user specified language
translated_text = translate_text(extracted_text, target_language)
if translated_text:
    print(f"Translated text in {target_language}!")
    print(translated_text)
