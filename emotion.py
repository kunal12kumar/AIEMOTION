import spacy
import torch
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

    for emotion in emotions[0]:
        print(f"{emotion['label']}: {emotion['score']:.4f}")
        
    return jsonify({"status": "success", "data": data})

if __name__ == '__main__':
    app.run(debug=True)


