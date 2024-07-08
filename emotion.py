import spacy
import torch
import pyttsx3
from transformers import pipeline
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/data": {"origins": "http://localhost:8000"}})


@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    print(f"Received data: {data}")
    value=data.get('key')
    print(f"Value of 'key': {value}")
    # Process the data as needed
    

    
    # Load SpaCy model
    nlp = spacy.load("en_core_web_sm")

    # Load pre-trained emotion detection model
    emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

    def get_emotions(text):
        # Process the text with SpaCy
        doc = nlp(text)
        
        # Get emotion scores
        emotions = emotion_pipeline(text)
        
        return emotions

    # Example usage
    text = value
    emotions = get_emotions(text)
    print(emotions)
    for emotion in emotions[0]:
        print(f"{emotion['label']}: {emotion['score']:.4f}")
        
    # Initialize the TTS engine
    engine = pyttsx3.init()

    
        # Determine the dominant emotion
    emotion=emotions[0]
    dominant_emotion = max(emotion, key=lambda x: x["score"])

    # Your sentenced
    sentence = value
    

    # Set properties based on the dominant emotion
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"ID: {voice.id}, Name: {voice.name}")

# Set a specific voice (example using the first available voice)
    engine.setProperty('voice', voices[1].id)
    if dominant_emotion['label'] == 'joy':
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1.0)  # Volume of speech
    elif dominant_emotion['label'] == 'sadness':
        engine.setProperty('rate', 100)
        engine.setProperty('volume', 0.5)
    elif dominant_emotion['label'] == 'anger':
        engine.setProperty('rate', 200)
        engine.setProperty('volume', 0.8)
    elif dominant_emotion['label'] == 'fear':
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.6)
    elif dominant_emotion['label'] == 'surprise':
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 0.9)
    else:  # Neutral or any other emotion
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 0.7)

    # Convert the sentence to speech
    engine.say(sentence)
    engine.runAndWait()

        
    return jsonify({"status": "success", "data": data})


# Sample emotions and their respective probabilities


if __name__ == '__main__':
    app.run(debug=True)


