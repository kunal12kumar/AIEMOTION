import spacy
import torch
from transformers import pipeline

import spacy
from transformers import pipeline

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
text = "I am feeling very happy and excited today!"
emotions = get_emotions(text)

for emotion in emotions[0]:
    print(f"{emotion['label']}: {emotion['score']:.4f}")
