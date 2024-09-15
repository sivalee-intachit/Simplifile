import azure.cognitiveservices.speech as speechsdk
from extractData import *

extracted_text = getExtracted_Text()

# Azure Text-to-Speech credentials
subscription_key = "6a024812672640f99db4ba1f1f05c833"
subscription_region = "eastus"

# Create a Speech config
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=subscription_region)
speech_config.speech_synthesis_voice_name = "en-US-EmmaNeural"

# Create a Speech synthesizer
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Synthesize the extracted text
result = synthesizer.speak_text_async(extracted_text).get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print(f"Speech synthesized for text [{extracted_text[:100]}...]")  # Print first 100 chars for brevity
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
    print(f"CANCELED: Reason={cancellation_details.reason}")

    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print(f"CANCELED: ErrorCode={cancellation_details.error_code}")
        print(f"CANCELED: ErrorDetails=[{cancellation_details.error_details}]")
        print(f"CANCELED: Did you update the subscription info?")
