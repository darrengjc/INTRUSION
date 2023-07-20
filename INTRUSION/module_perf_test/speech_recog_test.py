import numpy as np
import speech_recognition as sr
from jiwer import wer
import pandas as pd
import vosk
import json

recog = sr.Recognizer()

recorded_audios = ["../INTRUSION/module_perf_test/snd1_1.wav", "../INTRUSION/module_perf_test/snd2_2.wav", "../INTRUSION/module_perf_test/snd3.wav"]
ground_truths_ggl = ["the moon is blue", "the alphabet does not exist", "the chicken crosses the road"]
ground_truths_vosk = ["the moon is blue", "the alphabet does not exist", "the chicken crosses the road"]

# Initialize the Vosk model for recogVosk
vosk_model_path = "../INTRUSION/module_perf_test/vosk-model-small-en-us-0.15"
vosk_model = vosk.Model(vosk_model_path)

def recogGoogle(audio):
    with sr.WavFile(audio) as source:
        audio_data = recog.record(source)
        recog.adjust_for_ambient_noise(source, duration=0.2)
        recognized_text = recog.recognize_google(audio_data)
        print("Google Recognized Text: ", recognized_text)
        return recognized_text

def recogVosk(audio):
    with sr.AudioFile(audio) as source:
        audio_data = recog.record(source)
        recog.adjust_for_ambient_noise(source, duration=0.2)
        audio_bytes = audio_data.get_wav_data()
        
        # Use the Vosk model for recognition
        recognizer = vosk.KaldiRecognizer(vosk_model, audio_data.sample_rate)
        recognizer.AcceptWaveform(audio_bytes)
        result = json.loads(recognizer.Result())
        if "text" in result:
            recognized_text = result["text"]
        else:
            recognized_text = ""
        print("Vosk Recognized Text: ", recognized_text)
        return recognized_text

def recognizerTest():
    results = []
    for audio_file, ground_truth_ggl, ground_truth_vosk in zip(recorded_audios, ground_truths_ggl, ground_truths_vosk):
        result_ggl = recogGoogle(audio_file)
        result_vosk = recogVosk(audio_file)

        error_ggl = wer(ground_truth_ggl, result_ggl)
        error_vosk = wer(ground_truth_vosk, result_vosk)

        results.append({
            "Audio File": audio_file,
            "Google WER%": round(error_ggl * 100, 2),
            "Vosk WER%": round(error_vosk * 100, 2)
        })

    df_results = pd.DataFrame(results)
    print(df_results)

    mean_abs_ggl = df_results["Google WER%"].abs().mean()
    mean_abs_vosk = df_results["Vosk WER%"].abs().mean()

    
    # Calculate the total average percentage for each column
    percent_ggl = mean_abs_ggl 
    percent_vosk = mean_abs_vosk

    print(f"Total Average WER Percentage for Google: {percent_ggl:.2f}%")
    print(f"Total Average WER Percentage for Vosk: {percent_vosk:.2f}%")

recognizerTest()
